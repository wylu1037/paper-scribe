#!/usr/bin/env node

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const skillName = 'paper-scribe';
const sourceDir = path.resolve(__dirname, '..', 'skill');

function usage() {
  return `Usage: paper-scribe-skill [options]

Install the paper-scribe Claude skill into your local Claude skills directory.

Options:
  --target <dir>  Skills root directory. Defaults to ~/.claude/skills
  --force         Replace an existing paper-scribe skill directory
  --dry-run       Show what would happen without writing files
  --help          Show this help
`;
}

function parseArgs(argv) {
  const options = {
    targetRoot: path.join(os.homedir(), '.claude', 'skills'),
    force: false,
    dryRun: false,
    help: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--target') {
      const value = argv[index + 1];
      if (!value || value.startsWith('--')) {
        throw new Error('--target requires a directory');
      }
      options.targetRoot = expandHome(value);
      index += 1;
    } else if (arg === '--force') {
      options.force = true;
    } else if (arg === '--dry-run') {
      options.dryRun = true;
    } else if (arg === '--help' || arg === '-h') {
      options.help = true;
    } else {
      throw new Error(`Unknown option: ${arg}`);
    }
  }

  return options;
}

function expandHome(value) {
  if (value === '~') {
    return os.homedir();
  }
  if (value.startsWith('~/')) {
    return path.join(os.homedir(), value.slice(2));
  }
  return path.resolve(value);
}

function listFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...listFiles(fullPath));
    } else if (entry.isFile()) {
      files.push(fullPath);
    }
  }
  return files;
}

function copyDirectory(from, to) {
  fs.mkdirSync(to, { recursive: true });
  for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
    const sourcePath = path.join(from, entry.name);
    const targetPath = path.join(to, entry.name);
    if (entry.isDirectory()) {
      copyDirectory(sourcePath, targetPath);
    } else if (entry.isFile()) {
      fs.copyFileSync(sourcePath, targetPath);
    }
  }
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    process.stdout.write(usage());
    return 0;
  }

  if (!fs.existsSync(path.join(sourceDir, 'SKILL.md'))) {
    throw new Error(`Skill source not found: ${sourceDir}`);
  }

  const targetRoot = path.resolve(options.targetRoot);
  const targetDir = path.join(targetRoot, skillName);
  const exists = fs.existsSync(targetDir);
  const files = listFiles(sourceDir).map((file) => path.relative(sourceDir, file));

  console.log('paper-scribe skill installer');
  console.log('This is a community npx installer, not the official Claude plugin marketplace.');
  console.log(`Source: ${sourceDir}`);
  console.log(`Target: ${targetDir}`);
  console.log(`Files: ${files.length}`);

  if (options.dryRun) {
    console.log('Dry run only. No files were written.');
    for (const file of files) {
      console.log(`- ${file}`);
    }
    if (exists && !options.force) {
      console.log('Target already exists; a real install would require --force.');
    }
    return 0;
  }

  if (exists && !options.force) {
    throw new Error(`Target already exists: ${targetDir}\nRun again with --force to replace it.`);
  }

  if (exists) {
    fs.rmSync(targetDir, { recursive: true, force: true });
  }

  fs.mkdirSync(targetRoot, { recursive: true });
  copyDirectory(sourceDir, targetDir);

  console.log('Installed paper-scribe successfully.');
  console.log('Restart or reload Claude Code if the skill list was already loaded.');
}

try {
  process.exitCode = main();
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
