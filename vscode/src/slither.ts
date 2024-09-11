import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import { TextDecoder } from 'util';
import { ExtensionContext, Uri, window, workspace } from 'vscode';
import { LanguageClient, LanguageClientOptions, ServerOptions, TransportKind } from 'vscode-languageclient/node';

export async function createSlitherClient(context: ExtensionContext): Promise<LanguageClient> {
  const venvPath = path.join(context.extensionPath, '..', 'osmium-vyper-env');
  console.log('dossier du venv : ', venvPath);
  const pythonPath = path.join(venvPath, 'bin', 'python');

  if (!fs.existsSync(pythonPath)) {
    window.showErrorMessage(
      `L'interpréteur Python n'a pas été trouvé à l'emplacement : ${pythonPath}. Installation en cours ...`,
    );
    try {
      execSync(`python3.10 -m venv ${venvPath}`);
      execSync(`source ${venvPath}/bin/activate > log.txt`, { stdio: 'inherit', shell: '/bin/bash' });
      execSync(`${pythonPath} --version > log2.txt`, { stdio: 'inherit', shell: '/bin/bash' });
      execSync(`${pythonPath} -m pip install pygls `, { stdio: 'inherit', shell: '/bin/bash' });
      execSync(`${pythonPath} -m pip install vyper==0.3.7`, { stdio: 'inherit', shell: '/bin/bash' });
    } catch (error: any) {
      window.showErrorMessage(`Erreur lors de la création de l'environnement virtuel : ${error.message}`);
      console.error('Erreur détaillée :', error);
      throw new Error(`Erreur lors de la création de l'environnement virtuel : ${error.message}`);
    }
  } else {
    window.showInformationMessage("L'interpréteur Python trouvé");
  }

  const serverScript = context.asAbsolutePath(path.join('dist', 'slither-server', 'server.py'));

  const serverOptions: ServerOptions = {
    run: { command: pythonPath, args: [serverScript], transport: TransportKind.stdio },
    debug: { command: pythonPath, args: [serverScript], transport: TransportKind.stdio },
  };

  const clientOptions: LanguageClientOptions = {
    documentSelector: [{ scheme: 'file', language: 'vyper', pattern: '**/*.vy' }],
    synchronize: {
      fileEvents: workspace.createFileSystemWatcher('**/.solidhunter.json'),
    },
  };

  const client = new LanguageClient(
    'osmium-slither-vyper',
    'Osmium Slither Language Server for Vyper',
    serverOptions,
    clientOptions,
  );

  console.log('client', client);

  client.onRequest('osmium/getContent', async (params: { uri: string }) => {
    const contentUint8 = await workspace.fs.readFile(Uri.parse(params.uri));
    const content = new TextDecoder().decode(contentUint8);
    return {
      content,
    };
  });

  await client.start();

  return client;
}
