const { Console } = require("console");
const FastSpeedtest = require("fast-speedtest-api");
const FileSystem = require('fs');
 
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
 
speedtest.getSpeed().then(s => {
    writeFile(stampFileName('Speedtest'), s);
    console.log(`Speed: ${s} Mbps`);
}).catch(e => {
	writeFile(stampFileName('Speedtest'), 0);
    console.error(e.message);
});

function stampFileName(topic)
{
    const d = new Date();
    const day = d.getDate();
    const month = d.getMonth();
    const year = d.getFullYear();

    return topic + '_' + day + month + year + '.json';
}

function writeFile(fileName, speed)
{
    const dateStamp = Date.now();
    if(!FileSystem.existsSync(fileName))
    {
        FileSystem.writeFileSync(fileName, '{}');
        console.log('Created File: ' + fileName);
    }
    let data = JSON.parse(FileSystem.readFileSync(fileName, {encoding:'utf8', flag:'r'}));
    data[Math.round(parseInt(dateStamp) / 1000)] = speed;
    FileSystem.writeFileSync(fileName, JSON.stringify(data));
}