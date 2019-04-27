var dbURL = "http://127.0.0.1:5000/api/";

export function summonerInfoUrl(server, summonerName) {
  return dbURL + server + "/" + summonerName + "/overview";
}

export function accountIdUrl(server, summonerName) {
  return dbURL + server + "/" + summonerName + "/accountId";
}