import React, { useState, useEffect } from 'react';

const TestInterface = () => {
    const [defaultStyles, setDefaultStyles] = useState([]);
    const [contentImageUrl, setContentImageUrl] = useState('');

    const apiUrl = 'http://localhost:8080/api'; // Update with your Flask API URL if different
    const resourceUrl = 'http://localhost:8080';

    // Function to fetch default styles from the API
    const fetchDefaultStyles = () => {
        fetch(`${apiUrl}/default-styles`)
            .then(response => response.json())
            .then(data => setDefaultStyles(data.styles))
            .catch(error => console.error('Error:', error));
    };

    // Function to upload an image
    const uploadImage = () => {
        const formData = new FormData();
        const imageFile = document.getElementById("imageInput").files[0];
        formData.append("image", imageFile);

        fetch(`${apiUrl}/upload/content`, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            setContentImageUrl(data.contentImageUrl);
        })
        .catch(error => console.error('Error:', error));
    };

    // Function to perform style transfer
    const performStyleTransfer = () => {
        // Implement the logic for performing style transfer
        // You can use contentImageUrl and selectedStyleUrl states here
    };

    // Load default styles when the component mounts
    useEffect(() => {
        fetchDefaultStyles();
    }, []);

    // Function to select a style
    const selectStyle = (styleUrl) => {
        console.log('Selected Style:', styleUrl);
        // You can perform any other action here when a style is selected
    };

    // Function to generate style image
    const generateStyleImage = () => {
        // Implement the logic for generating style image
        // You can use the styleCaption state here
    };

    return (
        <div>
            <h1>Style Transfer Testing Interface</h1>

            <h2>Upload Content Image</h2>
            <input type="file" id="imageInput" name="image" required />
            <button type="button" onClick={uploadImage}>Upload Image</button>
            <p id="uploadResult"></p>

            {/* Display uploaded content image */}
            {contentImageUrl && (
                <div>
                    <h2>Uploaded Content Image</h2>
                    <img src={contentImageUrl} alt="Uploaded Content Image" />
                </div>
            )}

            <h2>Select Default Styles</h2>
            <div id="styleOptions">
                {defaultStyles.map((style, index) => (
                    <button key={index} onClick={() => selectStyle(style.url)}>
                        {style.url}
                    </button>
                ))}
            </div>

            {/* Display default style images */}
            <h2>Default Style Images</h2>
            <div id="default-styles">
                {defaultStyles.map((style, index) => (
                    <img key={index} src={style.url} alt={`Default Style ${index + 1}`} />
                ))}
            </div>

            <h2>Generate Style Image via ChatGPT</h2>
            <textarea id="styleCaption" rows="4" cols="50" placeholder="Enter description for the style image..."></textarea><br />
            <button type="button" onClick={generateStyleImage}>Generate Style Image</button>
            <p id="generationResult"></p>

            <h2>Perform Style Transfer</h2>
            <button type="button" onClick={performStyleTransfer}>Transfer Style</button>
            <p id="transferResult"></p>
        </div>
    );
};

export default TestInterface;
