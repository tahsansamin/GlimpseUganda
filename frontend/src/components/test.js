import React from "react";
import apiClient from "../api";

const App = () => {
    const fetchData = async () => {
        try {
            const response = await apiClient.get('/some-endpoint');
            console.log(response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
    return (<div>
            <h1>Test Component</h1>
            <button onClick={fetchData}>Fetch Data</button>
        </div> 
    );

}