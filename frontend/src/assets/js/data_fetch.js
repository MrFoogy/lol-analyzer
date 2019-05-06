var dbURL = "http://127.0.0.1:5000/api/";

export function summonerInfoUrl(server, summonerName) {
  return dbURL + server + "/" + summonerName + "/overview";
}

export function accountIdUrl(server, summonerName) {
  return dbURL + server + "/" + summonerName + "/account";
}

export function championMasteryUrl(server, summonerId) {
  return dbURL + server + "/" + summonerId + "/champion/mastery";
}

export function matchListUrl(server, accountId) {
  return dbURL + server + "/" + accountId + "/matchlist";
}

export function matchDetailsUrl(server, matchId) {
  return dbURL + server + "/match/" + matchId;
}

export function matchKillsUrl(server, matchId) {
  return dbURL + server + "/match_timeline/" + matchId + "/timeline";
}