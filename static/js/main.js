document.addEventListener('DOMContentLoaded', () => {
    // Setup Drop Zones
    const dropZones = document.querySelectorAll('.drop-zone');

    dropZones.forEach(zone => {
        const fileInput = zone.querySelector('.file-input');
        const selectedFileDiv = zone.parentNode.querySelector('.selected-file');
        const fileNameSpan = selectedFileDiv ? selectedFileDiv.querySelector('.file-name') : null;

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            zone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Highlight drop zone when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            zone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            zone.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            zone.classList.add('dragover');
        }

        function unhighlight(e) {
            zone.classList.remove('dragover');
        }

        // Handle dropped files
        zone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length) {
                fileInput.files = files; // Assign files to input
                updateFileList(files[0]);
            }
        }

        // Handle selected files via click
        fileInput.addEventListener('change', function() {
            if (this.files.length) {
                updateFileList(this.files[0]);
            }
        });

        function updateFileList(file) {
            if (selectedFileDiv && fileNameSpan) {
                fileNameSpan.textContent = file.name;
                selectedFileDiv.style.display = 'flex';
                
                // Add a small bounce animation to the file name
                selectedFileDiv.style.animation = 'pulse 0.5s ease';
                setTimeout(() => {
                    selectedFileDiv.style.animation = '';
                }, 500);
            }
        }
    });
});
