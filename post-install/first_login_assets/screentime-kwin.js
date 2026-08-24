function report(win) {
    var cls = (win && win.resourceClass) ? win.resourceClass : "";
    callDBus("org.pearos.ScreenTime", "/Collector", "org.pearos.ScreenTime.Collector", "reportActiveWindow", cls);
}
workspace.windowActivated.connect(report);
if (workspace.activeWindow) report(workspace.activeWindow);
