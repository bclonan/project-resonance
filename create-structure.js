#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * Parse tree to a list of relative file and directory paths
 * @param {string} tree
 * @returns {{dirs: string[], files: string[]}}
 */
function parseTree(tree) {
    const lines = tree.split('\n').filter(Boolean);
    const stack = [];
    const dirs = new Set();
    const files = [];

    for (let raw of lines) {
        const line = raw.replace(/\r$/, '');
        const match = line.match(/^([ ││]+)?(├── |└── )?(.*)$/);
        if (!match) continue;
        const [, prefix, , item] = match;
        if (!item) continue;

        const depth = prefix ? (prefix.match(/ {4}|│ {3}/g) || []).length : 0;
        let name = item.trim();
        stack[depth] = name;
        stack.length = depth + 1;

        // Ignore connector only
        if (/^│+$/.test(name)) continue;

        const relPath = stack.slice(0, depth + 1).join(path.sep);
        if (name.endsWith('/')) {
            dirs.add(relPath.replace(/\/$/, '')); // Remove trailing slash
        } else {
            // Add all parent dirs for this file
            for (let i = 1; i < stack.length; ++i)
                dirs.add(stack.slice(0, i).join(path.sep));
            files.push(relPath);
        }
    }
    return {
        dirs: Array.from(dirs).filter(Boolean).sort((a, b) => a.length - b.length), // Shallow dirs first
        files
    };
}

/**
 * Create directories, ignoring if they exist
 */
function createDirs(dirs) {
    for (let dir of dirs) {
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
    }
}

/**
 * Create files (touch), ensuring parent dir exists
 */
function createFiles(files) {
    for (let file of files) {
        const parent = path.dirname(file);
        if (parent && !fs.existsSync(parent)) fs.mkdirSync(parent, { recursive: true });
        if (!fs.existsSync(file)) fs.writeFileSync(file, '');
    }
}

// CLI usage: node create-structure.js tree.txt
if (require.main === module) {
    const inputFile = process.argv[2];
    if (!inputFile) {
        console.error('Usage: node create-structure.js <input-file>');
        process.exit(1);
    }
    const tree = fs.readFileSync(inputFile, 'utf-8');
    const { dirs, files } = parseTree(tree);

    createDirs(dirs);
    createFiles(files);

    console.log('✅ Directory structure created (robust version).');
}

module.exports = { parseTree, createDirs, createFiles };
