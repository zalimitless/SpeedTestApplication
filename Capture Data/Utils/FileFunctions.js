const FileSystem = require('fs');

function stampFileName(topic, date)
{
    const day = date.getDate();
    const month = date.getMonth();
    const year = date.getFullYear();

    const weekday = date.getDay();
    const weOrW = weekday > 4 ? 'we' : 'w';

    return topic + '_' + day + month + year + '_' + weOrW +'.csv';
}

function writeFile(fileName, value)
{
    const dateStamp = Date.now();
    if(!FileSystem.existsSync(fileName))
    {
        FileSystem.writeFileSync(fileName,"Time;Value\n");
        console.log('Created File: ' + fileName);
    }
    var output = (Math.round(parseInt(dateStamp)).toString() + ';' + (value).toString());
    FileSystem.appendFileSync(fileName, output + "\n")
}

exports.stampFileName = stampFileName;
exports.writeFile = writeFile;