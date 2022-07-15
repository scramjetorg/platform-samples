#!/usr/bin/env node

const PrePack = require("./lib/pre-pack");
const prePack = new PrePack({
    outDir: process.env.OUT_DIR || "dist",
    localPkgs: process.env.LOCAL_PACKAGES,
    flatPkgs: process.env.FLAT_PACKAGES,
    localCopy: process.env.LOCAL_COPY,
    noInstall: process.env.NO_INSTALL,
    public: process.env.MAKE_PUBLIC,
    distPackDir: process.env.DIST_PACK_DIR
});

prePack.build()
    .catch(e => {
        console.error(e.stack);
        process.exitCode = e.exitCode || 10;
    });
