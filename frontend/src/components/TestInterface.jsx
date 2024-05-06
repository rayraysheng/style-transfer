import React, { useState, useEffect } from 'react';
import './style.css';

const TestInterface = () => {
    const [defaultStyles, setDefaultStyles] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const [contentImageUrl, setContentImageUrl] = useState('');
    const [styleImageUrl, setStyleImageUrl] = useState('');

    const [stylizedImageUrl, setStylizedImageUrl] = useState('');
    const [blendedImageUrl, setBlendedImageUrl] = useState('');


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
        if (!contentImageUrl || !styleImageUrl) {
            alert("Please ensure both content and style images are selected.");
            return;
        }

        setIsLoading(true);

        fetch(`${apiUrl}/synthesis`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contentImageUrl: contentImageUrl,
                styleImageUrl: styleImageUrl
            })
        })
        .then(response => response.json())
        .then(data => {
            setStylizedImageUrl(data.stylizedImageUrl);
            setBlendedImageUrl(data.blendedImageUrl);
            setIsLoading(false);
            console.log(data); // You may want to do something with this data
        })
        .catch(error => {
            console.error('Error:', error);
            setIsLoading(false);
        });
    };

    // Load default styles when the component mounts
    useEffect(() => {
        fetchDefaultStyles();
    }, []);

    // Function to select a style
    const selectStyle = (styleUrl) => {
        console.log('Selected Style:', styleUrl);
        setStyleImageUrl(styleUrl);
    };

    // Function to generate style image
    const generateStyleImage = () => {
        const styleCaption = document.getElementById("styleCaption").value;
        if (!styleCaption.trim()) {
            alert("Please enter a description for the style image.");
            return;
        }
    
        setIsLoading(true);
    
        fetch(`${apiUrl}/style-generation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ caption: styleCaption }),
        })
        .then(response => response.json())
        .then(data => {
            setStyleImageUrl(data.styleImageUrl);
            setIsLoading(false);
        })
        .catch(error => {
            console.error('Error:', error);
            setIsLoading(false);
        });
    };
    

    return (
        <div className='wrapper'>
            {/* <h1 className="">Style Transfer Testing Interface</h1> */}
            <div className='content-image-container'>
                <div className='title-container'>
                    <div className='title'>
                        <img className="logo-img" src="images\logo.png" alt="Logo"/> 
                        <h1>PIXEL FUSION</h1>
                    </div>
                </div>
                <div className='image-upload-container'>
                    <h2>Upload Content Image</h2> 
                    <input type="file" id="imageInput" name="image" required />
                    <button type="button" onClick={uploadImage}>Upload Image</button>
                    {/* <div id="preview"> */}
                        <p id="uploadResult"></p>
                        {/* Display uploaded content image */}
                        {contentImageUrl && (
                            <div id="preview">
                                <img src={contentImageUrl} alt="Uploaded Content Image" />
                            </div>
                        )}
                    {/* </div> */}
                </div>
            </div>

            <div className='image-mood-container'>
                <h1>What is the Image Mood?</h1>
                <div className="mood-container">
                    <div className="left-section">
                        <h2>Select Default Styles</h2>
                        <div className='mood-buttons'>
                            <div id="styleOptions">
                                {defaultStyles.map((style, index) => (
                                    <button key={index} onClick={() => selectStyle(style.url)}>
                                        {style.url}
                                    </button>
                                ))}
                            </div>

                            {/* Display default style images */}
                            {/* <h2>Default Style Images</h2>
                            <div id="default-styles">
                                {defaultStyles.map((style, index) => (
                                    <img key={index} src={style.url} alt={`Default Style ${index + 1}`} />
                                ))}
                            </div> */}
                        </div>
                        
                        <h2>Generate Style Image via ChatGPT</h2>
                        <div className='chat-container'>
                            <textarea id="styleCaption" rows="4" cols="50" placeholder="Enter description for the style image..."></textarea><br />
                            <button type="button" onClick={generateStyleImage}>Generate Style Image</button>
                        </div>
                    </div>
                    
                    <div className='right-section'>
                        <div id="imagePlaceholder" className="image-placeholder">
                            {isLoading && <p>Generating style image, please wait...</p>} {/* Display loading message when generating image */}
                            {styleImageUrl && (
                                <div>
                                    <h2>Generated Style Image</h2>
                                    <img src={styleImageUrl} alt="Generated Style" />
                                </div>
                            )}
                            <p id="generationResult"></p>
                        </div>

                        <h2>Perform Style Transfer</h2>
                        <button type="button" onClick={performStyleTransfer}>Transfer Style</button>
                        <p id="transferResult"></p>
                    </div>
                </div>
            </div>
           
            <div className="results-section">
                <div className="results-container">
                    <h1>Result Image</h1>
                    <div id="resultsPlaceholder" className="results-placeholder">
                        {/* Display the stylized and blended images if available */}
                        <div style={{ display: 'flex', justifyContent: 'center', gap: '20px' }}>
                            {stylizedImageUrl && (
                                <div style={{ flex: 1 }}>
                                    <h3>Stylized Image</h3>
                                    <img src={stylizedImageUrl} alt="Stylized Image" style={{ width: '100%', height: 'auto' }} />
                                </div>
                            )}
                            {blendedImageUrl && (
                                <div style={{ flex: 1 }}>
                                    <h3>Blended Image</h3>
                                    <img src={blendedImageUrl} alt="Blended Image" style={{ width: '100%', height: 'auto' }} />
                                </div>
                            )}
                        </div>
                    </div>
                    <div id="caption" className="caption">Caption: Default Caption</div>
                </div>
            </div>
        </div>
    );
};

export default TestInterface;
