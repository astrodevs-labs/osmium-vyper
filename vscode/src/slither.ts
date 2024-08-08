import * as path from 'path';
import { TextDecoder } from 'util';
import { ExtensionContext, Uri, workspace } from 'vscode';
import { LanguageClient, LanguageClientOptions, ServerOptions, TransportKind } from 'vscode-languageclient/node';

export async function createSlitherClient(context: ExtensionContext): Promise<LanguageClient> {
  // The server is implemented in node
  const serverScript = context.asAbsolutePath(path.join('dist', 'slither-server', 'server.py'));
  const pythonPath = context.asAbsolutePath(path.join('..', 'osmium-vyper-env', 'bin', 'python')); // Chemin vers l'interpréteur Python de l'environnement virtuel

  console.log('serverScript', serverScript);
  console.log('pythonPath', pythonPath);

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
