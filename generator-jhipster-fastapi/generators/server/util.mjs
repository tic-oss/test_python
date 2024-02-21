import fs from 'fs';
import path from 'path';
import chalk from 'chalk';

let communications = [];

export function deleteUnwantedFiles() {
  const generatedFilesDir = this.destinationPath();
  const generatedFiles = fs.readdirSync(generatedFilesDir);
  generatedFiles.forEach(file => {
    if (file !== '.yo-rc.json' && file !== 'comm.yo-rc.json') {
      const filePath = path.join(generatedFilesDir, file);
      if (fs.existsSync(filePath)) {
        if (fs.statSync(filePath).isDirectory()) {
          fs.rmdirSync(filePath, { recursive: true });
        } else {
          fs.unlinkSync(filePath);
        }
        this.log(chalk.red(`  Deleted`) + `  ${this.destinationPath(filePath)}`);
      }
    }
  });
}

export function loadCommunicationConfigs() {
  const path = this.destinationPath('../' + this.jhipsterConfig.baseName);
  if (this.fs.exists(`${path}/comm.yo-rc.json`)) {
    try {
      const allCommunication = JSON.parse(fs.readFileSync(`${path}/comm.yo-rc.json`));
      communications = allCommunication;
    } catch (err) {
      throw new Error(`Cannot parse the file comm.yo-rc.json in '${this.directoryPath}'`);
    }
  }
}

export function findConfigByBaseName(baseName) {
  const result = [];
  for (const communication of communications) {
    if (communication.client === baseName) {
      result.push({
        server: communication.server,
        type: communication.type,
        framework: communication.framework,
      });
    }
    if (communication.server === baseName) {
      result.push({
        client: communication.client,
        type: communication.type,
        framework: communication.framework,
      });
    }
  }

  return result;
}

export { communications };