var dbURL = "http://127.0.0.1:5000/api/";

export function summonerInfoUrl(server, summonerName) {
  return dbURL + server + "/summoner/" + summonerName + "/overview";
}

export function accountIdUrl(server, summonerName) {
  return dbURL + server + "/summoner/" + summonerName + "/account";
}

export function championMasteryUrl(server, summonerId) {
  return dbURL + server + "/summoner/" + summonerId + "/champion/mastery";
}

export function matchListUrl(server, accountId) {
  return dbURL + server + "/account/" + accountId + "/matchlist";
}

export function matchDetailsUrl(server, matchId) {
  return dbURL + server + "/match/" + matchId;
}

export function matchTimelineUrl(server, matchId) {
  return dbURL + server + "/match_timeline/" + matchId;
}

export function combinedTimelineUrl(server, accountId) {
  return dbURL + server + "/account/" + accountId + "/combined_timeline";
}

export function fullTimelineUrl(server, accountId) {
  return dbURL + server + "/account/" + accountId + "/full_timeline";
}