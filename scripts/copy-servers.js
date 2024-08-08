const fs = require('fs');

const outputFolder = __dirname + '/../vscode/dist';

fs.readdir('servers', { withFileTypes: true }, (err, dirs) => {
  if (err) {
    console.error(err);
    return;
  }
  const servers = dirs.filter((file) => file.isDirectory()).map((file) => file.name);
  servers.forEach((serverDir) => {
    fs.readdir(`servers/${serverDir}/src`, { withFileTypes: true }, (err, entries) => {
      if (err) {
        console.error(err);
        return;
      }
      const files = entries.filter((file) => file.isFile()).map((file) => file.name);
      console.log('Copying server binary to vscode/dist', files);
      fs.mkdir(`${outputFolder}/${serverDir}/`, { recursive: true }, (err) => {
        if (err) {
          return console.error(err);
        }

        fs.copyFile(
          `servers/${serverDir}/src/${files}`,
          `${outputFolder}/${serverDir}/${files}`,
          (err) => {
            if (err) {
              console.error(err);
            }
          }
        );
      });
    });
  });
});
