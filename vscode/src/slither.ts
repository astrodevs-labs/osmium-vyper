import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import { TextDecoder } from 'util';
import { ExtensionContext, Uri, window, workspace } from 'vscode';
import { LanguageClient, LanguageClientOptions, ServerOptions, TransportKind } from 'vscode-languageclient/node';

export async function createSlitherClient(context: ExtensionContext): Promise<LanguageClient> {
  const venvPath = path.join(context.extensionPath, '..', 'osmium-vyper-env');
  const pythonPath = path.join(venvPath, 'bin', 'python');

  if (!fs.existsSync(pythonPath)) {
    window.showErrorMessage(
      `L'interpréteur Python n'a pas été trouvé à l'emplacement : ${pythonPath}. Installation en cours ...`,
    );
    try {
      execSync(`python3 -m venv ${venvPath}`);
    } catch (error: any) {
      window.showErrorMessage(`Erreur lors de la création de l'environnement virtuel : ${error.message}`);
      throw new Error(`Erreur lors de la création de l'environnement virtuel : ${error.message}`);
    }
  } else {
    window.showInformationMessage("L'interpréteur Python trouvé");
  }

  // The server is implemented in node
  const serverScript = context.asAbsolutePath(path.join('dist', 'slither-server', 'server.py'));

  // If the extension is launched in debug mode then the debug server options are used
  // Otherwise the run options are used
  const serverOptions: ServerOptions = {
    run: { command: pythonPath, args: [serverScript], transport: TransportKind.stdio },
    debug: { command: pythonPath, args: [serverScript], transport: TransportKind.stdio },
  };

  // Options to control the language client
  const clientOptions: LanguageClientOptions = {
    // Register the server for plain text documents
    documentSelector: [{ scheme: 'file', language: 'python' }],
    synchronize: {
      // Notify the server about file changes to '.clientrc files contained in the workspace
      fileEvents: workspace.createFileSystemWatcher('**/.solidhunter.json'),
    },
  };

  // Create the language client and start the client.
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

  // Start the client. This will also launch the server
  await client.start();

  return client;
}
