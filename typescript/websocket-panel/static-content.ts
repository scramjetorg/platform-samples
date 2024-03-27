import { ParsedMessage } from "@scramjet/types";
import { readFileSync } from "fs";
import { ServerResponse } from "http";
import { resolve } from "path";

function getContentType(filename: string = ".") {
    const extension = filename.split('.')!.pop()!.toLowerCase();
    let contentType = '';

    switch(extension) {
        case 'txt': contentType = 'text/plain'; break;
        case 'html': contentType = 'text/html'; break;
        case 'css': contentType = 'text/css'; break;
        case 'js': contentType = 'application/javascript'; break;
        case 'json': contentType = 'application/json'; break;
        case 'jpg': case 'jpeg': contentType = 'image/jpeg'; break;
        case 'png': contentType = 'image/png'; break;
        case 'gif': contentType = 'image/gif'; break;
        default: contentType = 'application/octet-stream';
    }

    return contentType;
}

export function staticContent(req: ParsedMessage, res: ServerResponse) {
    if (req.method !== "GET") {
        return "method not allowed";
    }

    req.params ||= {};
    req.params.path ||= "index.html";

    const path = req.params.path;

    let mime = "";
    let contents = "";

    try {
        contents = readFileSync(resolve(__dirname, `./www/${path}`), { encoding: 'utf8', flag: 'r' });
        mime = getContentType(path);
    } catch (e: any) {
        contents = e.toString()
        mime = "text/plain";
    }

    res.writeHead(200, "OK", {
        contentType: mime
    });

    res.write(contents);
    res.end();
}
