const { pingTargets } = require("../PingTest");
const { stampFileName, writeFile } = require("./FileFunctions");

const delay = ms => new Promise(resolve => setTimeout(resolve, ms))

async function pingRounds(rounds, ip, date, delayTime=500)
{
    for (var round = 0; round <= rounds; round++)
    {
        await delay(delayTime);
        pingTargets(ip, logResults, date);
    }
}

async function ping(ip, date, delayTime=500)
{
    await delay(delayTime);
    pingTargets(ip, logResults, date);
}

function logResults(status, message, date)
{
    if (status === -1)
    {
        console.log("Error", message);
        return;
    }

    var filename = stampFileName("Ping", date);
    writeFile(filename, message);
}

exports.pingRounds = pingRounds;
exports.delay = delay;
exports.ping = ping;