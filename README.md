# Pre-Sales Funnel Dashboard

A visualization dashboard for tracking clients through the sales pipeline.

## Overview

This pre-sales funnel dashboard allows you to:

1. Visualize clients at different stages of the sales funnel
2. Track client progress from research to closed deals
3. Manage client information and update their status as they move through the funnel
4. Filter and search clients
5. Export client data to CSV format

## Features

- **Interactive Funnel Chart**: Visual representation of clients at each pipeline stage
- **Client Management**: Add, edit, and delete client records
- **Stage Management**: Easily update client stages as they progress through the sales funnel
- **Data Persistence**: Client data is saved to local storage
- **Statistics**: View total clients, potential value, and conversion rates
- **Responsive Design**: Works on both desktop and mobile devices
- **Export Functionality**: Export your data to CSV for further analysis

## How to Use

1. **View the Funnel**: The left side of the dashboard shows a funnel chart depicting how many clients are at each stage.

2. **Manage Clients**: The right side shows a list of all clients.
   - Click on a client to view/edit details
   - Use the "+" button to add new clients
   - Use filters to find specific clients

3. **Update Client Stage**: 
   - Click the "exchange" icon next to a client to quickly change their status
   - Or edit the client record to update their stage

4. **Export Data**: Click the "Export Data" button to download your client data as a CSV file

## Sales Funnel Stages

The dashboard tracks the following stages:

1. **Research**: Initial research on potential clients
2. **Approached**: Initial contact made with the client
3. **First Presentation**: First presentation/meeting completed
4. **Interested**: Client has expressed interest
5. **Multiple Presentations**: Multiple (3-4) presentations completed
6. **Proposal**: Formal proposal submitted
7. **Negotiation**: In negotiation phase
8. **Order**: Order received, processing
9. **Closed**: Deal successfully closed

## Getting Started

To use this dashboard:

1. Simply open the `index.html` file in any modern web browser
2. Start adding your clients or use the provided sample data
3. Data is automatically saved to your browser's local storage

## Technical Details

This application uses:
- HTML5, CSS3, and JavaScript
- D3-funnel for funnel visualization
- Font Awesome for icons
- LocalStorage for data persistence
- Responsive CSS grid layout

No server or installation required - this is a completely client-side application.

## Data Privacy

All client data is stored locally in your browser's storage and is not transmitted to any server.
