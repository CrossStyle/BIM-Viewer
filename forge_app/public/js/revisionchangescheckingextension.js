class RevisionChangesCheckingExtension extends Autodesk.Viewing.Extension {
    constructor(viewer, options) {
        super(viewer, options);
        this._group = null;
        this._button = null;
    }

    load() {
        console.log('RevisionChangesCheckingExtension has been loaded');
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
        console.log('RevisionChangesCheckingExtension has been unloaded');
        return true;
    }

    createPDF(imgData) {
        var doc = new jsPDF()
        doc.setFontSize(20)
        doc.text(35, 25, 'ForgeViewer PDF report');
        doc.addImage(imgData, 'JPEG', 10, 40, 180, 80);
        doc.save('revision_changes.pdf')
    }


    onToolbarCreated() {
        // Create a new toolbar group if it doesn't exist
        this._group = this.viewer.toolbar.getControl('allMyAwesomeExtensionsToolbar');
        if (!this._group) {
            this._group = new Autodesk.Viewing.UI.ControlGroup('allMyAwesomeExtensionsToolbar');
            this.viewer.toolbar.addControl(this._group);
        }

        // Add a new button to the toolbar group
        this._button = new Autodesk.Viewing.UI.Button('RevisionChangesCheckingExtensionButton');
        this._button.onClick = (ev) => {
            // Execute an action here
            // Check if the panel is created or not

        this.viewer.getScreenShot()
  


        };
        this._button.setToolTip('Screen Shoot Extension');
        this._button.addClass('modelRevisionChangesCheckingExtensionExtensionIcon');
        this._group.addControl(this._button);
    }
}

    // Get the full image
    // viewer.getScreenShot(viewer.container.clientWidth, viewer.container.clientHeight, function (blobURL) {
    //     screenshot.src = blobURL;
    // });}

Autodesk.Viewing.theExtensionManager.registerExtension('RevisionChangesCheckingExtension', RevisionChangesCheckingExtension);
