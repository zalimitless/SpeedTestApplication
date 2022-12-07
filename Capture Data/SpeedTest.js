const FastSpeedtest = require("fast-speedtest-api");
const { stampFileName, writeFile } = require("./Utils/FileFunctions");
const { pingRounds, ping } = require("./Utils/PingFunctions");

// Visit fast.com and check the network for the token. It should be in the URL.
// Or go into the code and search for the keyword "Token" until you find it!
let speedtest = new FastSpeedtest({
    token: "YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm", // This is the default Token
    verbose: false, // default: false
    timeout: 10000, // default: 5000
    https: true, // default: true
    urlCount: 5, // default: 5
    bufferSize: 8, // default: 8
    unit: FastSpeedtest.UNITS.Mbps // default: Bps
});

var done = false;

const d = new Date();

async function doSpeedTest()
{

    speedtest.getSpeed().then(s => {
        writeFile(stampFileName('Speedtest', d), s);
        console.log(`Speed: ${s} Mbps`);
        done = true;
    }).catch(e => {
        writeFile(stampFileName('Speedtest', d), 0);
        console.error(e.message);
        done = true;
    });
}

async function pingLoop()
{
    while(!done)
    {
        await ping('8.8.8.8', d, 500);
    }
}
// pingRounds(10, '8.8.8.8', d, 50)
Promise.all([doSpeedTest(), pingLoop()])