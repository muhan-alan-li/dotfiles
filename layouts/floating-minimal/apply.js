// floating-minimal — Plasma 6 live layout
// Applied through org.kde.PlasmaShell.evaluateScript.
//
// Top panel:  thin, floating, translucent; clock - media - tray - power.
// Bottom dock: centered floating pill; icons - virtual desktops - app grid.

var dock = null;
var top = null;

panels().forEach(function (p) {
    var types = p.widgets().map(function (w) { return w.type; });
    if (types.indexOf("org.kde.plasma.icontasks") !== -1) {
        dock = p;
    } else {
        top = p;
    }
});

if (!dock || !top) {
    print("ERROR: expected exactly two panels (dock + info bar)");
} else {

    // ---------- bottom dock ----------
    dock.location = "bottom";
    dock.alignment = "center";
    dock.lengthMode = "fit";
    dock.floating = true;
    dock.opacity = "translucent";
    dock.hiding = "none";
    dock.height = 48;

    // Drop the widgets that make the dock busy.
    dock.widgets().forEach(function (w) {
        if (w.type === "org.kde.plasma.showdesktop" ||
            w.type === "org.kde.plasma.marginsseparator") {
            w.remove();
        }
    });

    function ids(panel, type) {
        var result = [];
        panel.widgets().forEach(function (w) {
            if (w.type === type) { result.push(w.id); }
        });
        return result;
    }

    var dockOrder = [];
    dockOrder = dockOrder.concat(ids(dock, "org.kde.plasma.icontasks"));
    dockOrder = dockOrder.concat(ids(dock, "org.kde.plasma.pager"));
    dockOrder = dockOrder.concat(ids(dock, "org.kde.plasma.kickoff"));
    dock.widgets().forEach(function (w) {
        if (dockOrder.indexOf(w.id) === -1) { dockOrder.push(w.id); }
    });
    dock.currentConfigGroup = ["General"];
    // Do NOT call reloadConfig() here: Plasma rewrites AppletOrder from the
    // in-memory widget order when it reloads, undoing the reorder.
    dock.writeConfig("AppletOrder", dockOrder.join(";"));

    // ---------- top info strip ----------
    top.location = "top";
    top.alignment = "center";
    top.lengthMode = "fill";
    top.floating = true;
    top.opacity = "translucent";
    top.hiding = "none";
    top.height = 30;

    // Move the system monitors off the strip (they remain available as
    // desktop widgets if you want the "info cards" look).
    top.widgets().forEach(function (w) {
        if (w.type.indexOf("org.kde.plasma.systemmonitor") === 0) {
            w.remove();
        }
    });

    // Pull the MPRIS media controller out of the tray and onto the strip.
    if (ids(top, "org.kde.plasma.mediacontroller").length === 0) {
        top.addWidget("org.kde.plasma.mediacontroller");
    }

    var spacers = ids(top, "org.kde.plasma.panelspacer");
    var topOrder = [];
    topOrder = topOrder.concat(ids(top, "org.kde.plasma.digitalclock"));
    if (spacers.length) { topOrder.push(spacers.shift()); }
    topOrder = topOrder.concat(ids(top, "org.kde.plasma.mediacontroller"));
    if (spacers.length) { topOrder.push(spacers.shift()); }
    topOrder = topOrder.concat(ids(top, "org.kde.plasma.systemtray"));
    topOrder = topOrder.concat(ids(top, "org.kde.plasma.lock_logout"));
    top.widgets().forEach(function (w) {
        if (topOrder.indexOf(w.id) === -1) { topOrder.push(w.id); }
    });
    top.currentConfigGroup = ["General"];
    top.writeConfig("AppletOrder", topOrder.join(";"));

    print("floating-minimal applied: dock=" + dock.id + " top=" + top.id);
}
