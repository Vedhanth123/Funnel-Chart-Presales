// Store our client data
let clientsData = [];

// Define the sales funnel stages in order
const stages = [
  'Research',
  'Approached',
  'First Presentation',
  'Interested',
  'Multiple Presentations',
  'Proposal',
  'Negotiation',
  'Order',
  'Closed'
];

// Stage colors for the funnel chart
const stageColors = {
  'Research': '#ecf0f1',
  'Approached': '#3498db',
  'First Presentation': '#2ecc71',
  'Interested': '#27ae60',
  'Multiple Presentations': '#16a085',
  'Proposal': '#f1c40f',
  'Negotiation': '#f39c12',
  'Order': '#e74c3c',
  'Closed': '#2c3e50'
};

// For generating unique IDs
function generateUniqueId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Load data from local storage
function loadClientData() {
  const savedData = localStorage.getItem('presalesFunnelData');
  if (savedData) {
    clientsData = JSON.parse(savedData);
  } else {
    // Initialize with sample data if no data exists
    clientsData = getSampleClientData();
    saveClientData();
  }
  renderClientsList();
  renderFunnelChart();
}

// Save data to local storage
function saveClientData() {
  localStorage.setItem('presalesFunnelData', JSON.stringify(clientsData));
}

// Generate sample data for initial view
function getSampleClientData() {
  return [
    {
      id: generateUniqueId(),
      name: 'Acme Corporation',
      company: 'Acme Inc.',
      contact: 'John Doe | john.doe@acme.com | 555-1234',
      stage: 'Research',
      value: 10000,
      notes: 'Initial research phase, identified potential needs.',
      lastUpdated: new Date().toISOString()
    },
    {
      id: generateUniqueId(),
      name: 'TechSolutions',
      company: 'TechSolutions Ltd.',
      contact: 'Jane Smith | jane@techsolutions.com | 555-5678',
      stage: 'Approached',
      value: 25000,
      notes: 'Initial contact made, scheduled intro meeting.',
      lastUpdated: new Date().toISOString()
    },
    {
      id: generateUniqueId(),
      name: 'Global Industries',
      company: 'Global Industries Corp',
      contact: 'Mike Johnson | mike@globalind.com | 555-9012',
      stage: 'First Presentation',
      value: 50000,
      notes: 'Presented initial proposal, awaiting feedback.',
      lastUpdated: new Date().toISOString()
    },
    {
      id: generateUniqueId(),
      name: 'Innovative Solutions',
      company: 'Innovative Solutions Inc.',
      contact: 'Sarah Williams | sarah@innovative.com | 555-3456',
      stage: 'Interested',
      value: 75000,
      notes: 'Showed interest after presentation, discussing next steps.',
      lastUpdated: new Date().toISOString()
    },
    {
      id: generateUniqueId(),
      name: 'EcoFriendly',
      company: 'EcoFriendly Systems',
      contact: 'Robert Brown | robert@ecofriendly.com | 555-7890',
      stage: 'Multiple Presentations',
      value: 100000,
      notes: 'Had 3 presentations with different departments.',
      lastUpdated: new Date().toISOString()
    },
    {
      id: generateUniqueId(),
      name: 'DataCorp',
      company: 'DataCorp Analytics',
      contact: 'Emily Davis | emily@datacorp.com | 555-2345',
      stage: 'Proposal',
      value: 150000,
      notes: 'Formal proposal submitted, awaiting review.',
      lastUpdated: new Date().toISOString()
    },
    {
      id: generateUniqueId(),
      name: 'MegaCorp',
      company: 'MegaCorp International',
      contact: 'Alex Johnson | alex@megacorp.com | 555-6789',
      stage: 'Negotiation',
      value: 200000,
      notes: 'In final negotiations regarding price and terms.',
      lastUpdated: new Date().toISOString()
    },
    {
      id: generateUniqueId(),
      name: 'Star Enterprises',
      company: 'Star Enterprises LLC',
      contact: 'Thomas White | thomas@star.com | 555-0123',
      stage: 'Order',
      value: 250000,
      notes: 'Order received, processing paperwork.',
      lastUpdated: new Date().toISOString()
    },
    {
      id: generateUniqueId(),
      name: 'Premier Services',
      company: 'Premier Services Group',
      contact: 'Lisa Miller | lisa@premier.com | 555-4567',
      stage: 'Closed',
      value: 300000,
      notes: 'Deal closed successfully.',
      lastUpdated: new Date().toISOString()
    }
  ];
}

// Render the client list with filtering
function renderClientsList() {
  const clientList = document.getElementById('clientList');
  const searchQuery = document.getElementById('searchClient').value.toLowerCase();
  const stageFilter = document.getElementById('filterStage').value;
  
  // Clear the list
  clientList.innerHTML = '';
  
  // Filter clients
  const filteredClients = clientsData.filter(client => {
    const matchesSearch = 
      client.name.toLowerCase().includes(searchQuery) || 
      client.company.toLowerCase().includes(searchQuery);
    
    const matchesStage = stageFilter === 'all' || client.stage === stageFilter;
    
    return matchesSearch && matchesStage;
  });
  
  // Sort by stage (in the funnel order)
  filteredClients.sort((a, b) => {
    const stageOrderA = stages.indexOf(a.stage);
    const stageOrderB = stages.indexOf(b.stage);
    return stageOrderA - stageOrderB;
  });
  
  // Display clients
  filteredClients.forEach(client => {
    const clientDiv = document.createElement('div');
    clientDiv.className = 'client-item';
    clientDiv.dataset.id = client.id;
    
    // Convert stage name to CSS class name
    const stageClass = 'stage-' + client.stage.toLowerCase().replace(/\s+/g, '-');
    
    clientDiv.innerHTML = `
      <div class="client-info">
        <div class="client-name">${client.name}</div>
        <div class="client-company">${client.company}</div>
      </div>
      <div class="client-stage ${stageClass}">
        ${client.stage}
      </div>
      <div class="client-actions">
        <button class="edit-client" title="Edit client"><i class="fas fa-edit"></i></button>
        <button class="move-client" title="Change stage"><i class="fas fa-exchange-alt"></i></button>
        <button class="delete-client" title="Delete client"><i class="fas fa-trash"></i></button>
      </div>
    `;
    
    clientList.appendChild(clientDiv);
    
    // Add event listeners to action buttons
    const editBtn = clientDiv.querySelector('.edit-client');
    const moveBtn = clientDiv.querySelector('.move-client');
    const deleteBtn = clientDiv.querySelector('.delete-client');
    
    editBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      openEditClientModal(client.id);
    });
    
    moveBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      openMoveClientModal(client.id);
    });
    
    deleteBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (confirm(`Are you sure you want to delete ${client.name}?`)) {
        deleteClient(client.id);
      }
    });
    
    // Click on client item to view details
    clientDiv.addEventListener('click', () => {
      openEditClientModal(client.id);
    });
  });
  
  // Show message if no clients found
  if (filteredClients.length === 0) {
    clientList.innerHTML = '<div class="no-results">No clients found matching your criteria.</div>';
  }
}

// Function to render the funnel chart using D3-funnel
function renderFunnelChart() {
  // Group clients by stage and count
  const stageCounts = {};
  const stageValues = {};
  
  stages.forEach(stage => {
    stageCounts[stage] = 0;
    stageValues[stage] = 0;
  });
  
  clientsData.forEach(client => {
    stageCounts[client.stage] = (stageCounts[client.stage] || 0) + 1;
    stageValues[client.stage] = (stageValues[client.stage] || 0) + (client.value || 0);
  });
  
  // Prepare data for the funnel chart
  const data = stages.map(stage => ({
    label: `${stage}: ${stageCounts[stage]} clients`,
    value: stageCounts[stage],
    formattedValue: stageCounts[stage].toString(),
    backgroundColor: stageColors[stage]
  }));
  
  // Clear previous chart
  const chartContainer = document.getElementById('funnelChart');
  chartContainer.innerHTML = '';
  
  // Set up the funnel chart options
  const options = {
    chart: {
      width: chartContainer.offsetWidth,
      height: 400,
      animate: 200
    },
    block: {
      dynamicHeight: true,
      minHeight: 15,
      fill: {
        type: 'solid'
      }
    },
    tooltip: {
      enabled: true
    },
    label: {
      format: '{l}',
      fontSize: '14px'
    }
  };
  
  // Initialize the funnel chart
  const funnel = new D3Funnel('#funnelChart');
  funnel.draw(data, options);
  
  // Update stats
  renderFunnelStats();
}

// Render funnel statistics
function renderFunnelStats() {
  const statsContainer = document.getElementById('funnelStats');
  
  // Clear previous stats
  statsContainer.innerHTML = '';
  
  // Calculate statistics
  const totalClients = clientsData.length;
  const totalValue = clientsData.reduce((sum, client) => sum + (client.value || 0), 0);
  const conversionRate = calculateConversionRate();
  
  // Display statistics
  statsContainer.innerHTML = `
    <div class="stat-item">
      <div class="stat-value">${totalClients}</div>
      <div class="stat-label">Total Clients</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">$${formatNumber(totalValue)}</div>
      <div class="stat-label">Total Value</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">${conversionRate}%</div>
      <div class="stat-label">Conversion Rate</div>
    </div>
  `;
}

// Calculate conversion rate
function calculateConversionRate() {
  const advancedStages = ['Proposal', 'Negotiation', 'Order', 'Closed'];
  const clientsInAdvancedStages = clientsData.filter(client => 
    advancedStages.includes(client.stage)
  ).length;
  
  if (clientsData.length === 0) return "0";
  
  const rate = (clientsInAdvancedStages / clientsData.length) * 100;
  return rate.toFixed(1);
}

// Format numbers with commas
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Open the client modal for adding a new client
function openAddClientModal() {
  const modal = document.getElementById('clientModal');
  const modalTitle = document.getElementById('modalTitle');
  const form = document.getElementById('clientForm');
  
  // Reset the form and set for adding
  form.reset();
  document.getElementById('clientId').value = '';
  modalTitle.textContent = 'Add New Client';
  
  // Show the modal
  modal.style.display = 'block';
}

// Open the client modal for editing an existing client
function openEditClientModal(clientId) {
  const client = clientsData.find(c => c.id === clientId);
  if (!client) return;
  
  const modal = document.getElementById('clientModal');
  const modalTitle = document.getElementById('modalTitle');
  const form = document.getElementById('clientForm');
  
  // Fill the form with client data
  document.getElementById('clientId').value = client.id;
  document.getElementById('clientName').value = client.name;
  document.getElementById('clientCompany').value = client.company;
  document.getElementById('clientContact').value = client.contact || '';
  document.getElementById('clientStage').value = client.stage;
  document.getElementById('clientValue').value = client.value || '';
  document.getElementById('clientNotes').value = client.notes || '';
  
  modalTitle.textContent = 'Edit Client';
  
  // Show the modal
  modal.style.display = 'block';
}

// Open a simplified modal to just move a client to another stage
function openMoveClientModal(clientId) {
  const client = clientsData.find(c => c.id === clientId);
  if (!client) return;
  
  // Create a temporary selection element with the stages
  const select = document.createElement('select');
  stages.forEach(stage => {
    const option = document.createElement('option');
    option.value = stage;
    option.textContent = stage;
    if (stage === client.stage) option.selected = true;
    select.appendChild(option);
  });
  
  // Show a custom dialog for stage selection
  const newStage = prompt(`Change stage for ${client.name} (current: ${client.stage})`, client.stage);
  
  if (newStage && stages.includes(newStage)) {
    client.stage = newStage;
    client.lastUpdated = new Date().toISOString();
    saveClientData();
    renderClientsList();
    renderFunnelChart();
  }
}

// Save client data from the modal form
function saveClientFromForm() {
  const form = document.getElementById('clientForm');
  const clientId = document.getElementById('clientId').value;
  
  const clientData = {
    name: document.getElementById('clientName').value,
    company: document.getElementById('clientCompany').value,
    contact: document.getElementById('clientContact').value,
    stage: document.getElementById('clientStage').value,
    value: parseFloat(document.getElementById('clientValue').value) || 0,
    notes: document.getElementById('clientNotes').value,
    lastUpdated: new Date().toISOString()
  };
  
  // Add or update client
  if (clientId) {
    // Update existing client
    const index = clientsData.findIndex(c => c.id === clientId);
    if (index !== -1) {
      clientData.id = clientId;
      clientsData[index] = clientData;
    }
  } else {
    // Add new client
    clientData.id = generateUniqueId();
    clientsData.push(clientData);
  }
  
  // Save, update UI and close modal
  saveClientData();
  renderClientsList();
  renderFunnelChart();
  closeModal();
}

// Delete a client
function deleteClient(clientId) {
  clientsData = clientsData.filter(client => client.id !== clientId);
  saveClientData();
  renderClientsList();
  renderFunnelChart();
}

// Close the modal
function closeModal() {
  const modal = document.getElementById('clientModal');
  modal.style.display = 'none';
}

// Export data to CSV
function exportDataToCSV() {
  // Create CSV header
  const csvRows = [];
  const headers = ['Client Name', 'Company', 'Contact Info', 'Stage', 'Potential Value ($)', 'Notes', 'Last Updated'];
  csvRows.push(headers.join(','));
  
  // Add client data
  clientsData.forEach(client => {
    const row = [
      `"${client.name}"`,
      `"${client.company}"`,
      `"${client.contact || ''}"`,
      `"${client.stage}"`,
      client.value || 0,
      `"${(client.notes || '').replace(/"/g, '""')}"`,
      `"${new Date(client.lastUpdated).toLocaleString()}"`,
    ];
    csvRows.push(row.join(','));
  });
  
  // Create and download CSV file
  const csvString = csvRows.join('\n');
  const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.setAttribute('href', url);
  a.setAttribute('download', `presales_funnel_${new Date().toISOString().slice(0, 10)}.csv`);
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// Add event listeners when document is ready
document.addEventListener('DOMContentLoaded', () => {
  // Load data
  loadClientData();
  
  // Add event listeners to buttons
  document.getElementById('addClientBtn').addEventListener('click', openAddClientModal);
  document.getElementById('exportBtn').addEventListener('click', exportDataToCSV);
  
  // Modal close button
  document.querySelector('.close').addEventListener('click', closeModal);
  document.getElementById('cancelBtn').addEventListener('click', closeModal);
  
  // Close modal when clicking outside
  window.addEventListener('click', (event) => {
    const modal = document.getElementById('clientModal');
    if (event.target === modal) {
      closeModal();
    }
  });
  
  // Form submission
  document.getElementById('clientForm').addEventListener('submit', (e) => {
    e.preventDefault();
    saveClientFromForm();
  });
  
  // Search and filter functionality
  document.getElementById('searchClient').addEventListener('input', renderClientsList);
  document.getElementById('filterStage').addEventListener('change', renderClientsList);
  
  // Resize event for the chart
  window.addEventListener('resize', () => {
    renderFunnelChart();
  });
});
