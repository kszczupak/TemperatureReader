# Home Boiler Temperature Monitor

Boiler Temperature Monitor is a project which uses image processing to read temperature from home's central heating boiler. To achieve this: 
1. Static image is taken using Raspberry Pi Camera
1. Image is send through image processing pipeline (thresholding, opening etc.)
1. Processed image is passed to pre-trained SVM classifier to get numerical temperature value
1. Temperature value is published over WAMP protocol to crossbar router using PubSub
1. Front-end component receives temperature update, displays current temperature and historical temperature chart
