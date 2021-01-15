class SearchByIDExtension extends Autodesk.Viewing.Extension {
    constructor(viewer, options) {
        super(viewer, options);
        this._group = null;
        this._button = null;

    }

    load() {
        console.log('SearchByIDExtension has been loaded');
        return true;
    }

    unload() {
        // Clean our UI elements if we added any
        if (this._group) {
            this._group.removeControl(this._button);
            if (this._group.getNumberOfControls() === 0) {
                this.viewer.toolbar.removeControl(this._group);
            }
        }
        console.log('SearchByIDExtension has been unloaded');
        return true;
    }

    testing() {}

    onToolbarCreated() {
        // Create a new toolbar group if it doesn't exist
        this._group = this.viewer.toolbar.getControl('allMyAwesomeExtensionsToolbar');
        if (!this._group) {
            this._group = new Autodesk.Viewing.UI.ControlGroup('allMyAwesomeExtensionsToolbar');
            this.viewer.toolbar.addControl(this._group);
        }

        // var filter = new Autodesk.Viewing.UI.Filterbox('searchbox', this.testing)             
        // var controlGroupMobileInput = new Autodesk.Viewing.UI.ControlGroup('custom-toolbar-input');                  
        // controlGroupMobileInput.addControl(filter);

        // Add a new button to the toolbar group
        this._button = new Autodesk.Viewing.UI.Button('SearchByIDExtensionButton');
        this._button.onClick = (ev) => {
            // Execute an action here
            var name=prompt("请输入dBID","xxx"); // 弹出input框 	
            // alert(name);
            // console.log(name);
            // console.log(typeof(name));
            this.viewer.isolate(Number(name));
            this.viewer.fitToView(Number(name));
        };
        this._button.setToolTip('Search By ID Extension');
        this._button.addClass('searchByIDExtensionIcon');
        this._group.addControl(this._button);
    }
}

Autodesk.Viewing.theExtensionManager.registerExtension('SearchByIDExtension', SearchByIDExtension);
