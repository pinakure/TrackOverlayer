import { buildAuthorization } from "@retroachievements/api";

const userName = "{% username %}";
const webApiKey = "{% ra-api-key %";

const authorization = buildAuthorization({ userName, webApiKey });

const game = await getGame(authorization, { gameId: 14402 });

console.log(game)