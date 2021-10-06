process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0; // in case of SSL errors

const { codegen } = require('swagger-axios-codegen');

codegen({
  fileName: 'api.ts',
  methodNameMode: 'operationId',
  modelMode: 'class',
  // source: require('./api.json')
  remoteUrl: 'http://localhost:8000/swagger/?format=openapi'
}).catch(e => console.log(e));

