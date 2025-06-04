import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json

# Set page config
st.set_page_config(page_title="Pre-Sales Funnel Dashboard", layout="wide")

# Define funnel stages
FUNNEL_STAGES = [
    "Research",
    "Initial Contact", 
    "First Presentation",
    "Interested",
    "Multiple Presentations",
    "Order Stage",
    "Negotiation",
    "Closed Won",
    "Closed Lost"
]

# Color mapping for stages
STAGE_COLORS = {
    "Research": "#FF6B6B",
    "Initial Contact": "#4ECDC4", 
    "First Presentation": "#45B7D1",
    "Interested": "#96CEB4",
    "Multiple Presentations": "#FFEAA7",
    "Order Stage": "#DDA0DD",
    "Negotiation": "#98D8C8",
    "Closed Won": "#6BCF7F",
    "Closed Lost": "#FF7675"
}

# Initialize session state
if 'clients_data' not in st.session_state:
    # Sample data
    st.session_state.clients_data = pd.DataFrame({
        'Client Name': [
            'ABC Corp', 'XYZ Ltd', 'Tech Innovations', 'Global Solutions',
            'StartUp Inc', 'Enterprise Co', 'Digital Agency', 'Manufacturing Ltd',
            'Retail Chain', 'Finance Group', 'Healthcare Systems', 'Education Board',
            'Alpha Industries', 'Beta Solutions', 'Gamma Corp'
        ],
        'Stage': [
            'Research', 'Initial Contact', 'First Presentation', 'Interested',
            'Multiple Presentations', 'Order Stage', 'Negotiation', 'Closed Won',
            'Research', 'First Presentation', 'Interested', 'Closed Lost',
            'Initial Contact', 'Multiple Presentations', 'Order Stage'
        ],
        'Contact Person': [
            'John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Wilson',
            'David Brown', 'Lisa Davis', 'Tom Anderson', 'Emily Clark',
            'Robert Miller', 'Amanda Taylor', 'Chris Moore', 'Jessica White',
            'Mark Thompson', 'Rachel Green', 'Steve Rogers'
        ],
        'Email': [
            'john@abc.com', 'jane@xyz.com', 'mike@tech.com', 'sarah@global.com',
            'david@startup.com', 'lisa@enterprise.com', 'tom@digital.com', 'emily@mfg.com',
            'robert@retail.com', 'amanda@finance.com', 'chris@health.com', 'jessica@edu.com',
            'mark@alpha.com', 'rachel@beta.com', 'steve@gamma.com'
        ],
        'Deal Value': [
            50000, 75000, 120000, 200000, 30000, 500000, 80000, 150000,
            45000, 90000, 300000, 25000, 60000, 180000, 350000
        ],
        'Last Updated': [date.today() for _ in range(15)]
    })

if 'selected_stage' not in st.session_state:
    st.session_state.selected_stage = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

def create_interactive_funnel_chart(df):
    """Create interactive funnel visualization"""
    stage_counts = df['Stage'].value_counts()
    
    # Reorder according to funnel stages
    ordered_counts = []
    ordered_stages = []
    colors = []
    
    for stage in FUNNEL_STAGES:
        count = stage_counts.get(stage, 0)
        ordered_counts.append(count)
        ordered_stages.append(f"{stage}<br>({count} clients)")
        colors.append(STAGE_COLORS[stage])
    
    fig = go.Figure(go.Funnel(
        y=ordered_stages,
        x=ordered_counts,
        textinfo="value+percent initial",
        marker=dict(color=colors),
        connector=dict(line=dict(color="royalblue", dash="solid", width=2)),
        hovertemplate="<b>%{y}</b><br>Click to view clients<extra></extra>"
    ))
    
    fig.update_layout(
        title="Pre-Sales Funnel Overview (Click on any stage to view clients)",
        height=600,
        font=dict(size=12)
    )
    
    return fig

def create_stage_cards(df):
    """Create clickable stage cards"""
    stage_counts = df['Stage'].value_counts()
    
    st.markdown("### 🎯 Quick Stage Navigation")
    st.markdown("Click on any stage below to view clients in that stage:")
    
    # Create rows of 3 cards each
    stages_with_counts = [(stage, stage_counts.get(stage, 0)) for stage in FUNNEL_STAGES]
    
    for i in range(0, len(stages_with_counts), 3):
        cols = st.columns(3)
        for j, (stage, count) in enumerate(stages_with_counts[i:i+3]):
            with cols[j]:
                color = STAGE_COLORS[stage]
                # Create a card-like button
                if st.button(
                    f"**{stage}**\n\n{count} clients", 
                    key=f"card_{stage}",
                    help=f"Click to view all clients in {stage}",
                    use_container_width=True
                ):
                    st.session_state.selected_stage = stage
                    st.session_state.current_page = "Stage View"
                    st.rerun()
                
                # Add visual indicator
                st.markdown(
                    f'<div style="height: 5px; background-color: {color}; margin-top: -10px; margin-bottom: 20px;"></div>',
                    unsafe_allow_html=True
                )

def create_deal_value_chart(df):
    """Create deal value by stage chart"""
    stage_values = df.groupby('Stage')['Deal Value'].sum().reset_index()
    
    fig = px.bar(
        stage_values, 
        x='Stage', 
        y='Deal Value',
        color='Stage',
        color_discrete_map=STAGE_COLORS,
        title="Total Deal Value by Stage (Click bars to view clients)"
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400,
        showlegend=False
    )
    
    fig.update_traces(
        texttemplate='$%{y:,.0f}', 
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Total Value: $%{y:,.0f}<br>Click to view clients<extra></extra>"
    )
    
    return fig

def display_stage_clients(df, stage):
    """Display clients for a specific stage"""
    stage_clients = df[df['Stage'] == stage]
    
    st.markdown(f"## 📋 Clients in: {stage}")
    st.markdown(f"**{len(stage_clients)} clients** • **Total Value: ${stage_clients['Deal Value'].sum():,.0f}**")
    
    if st.button("← Back to Dashboard", key="back_to_dashboard"):
        st.session_state.current_page = "Dashboard"
        st.session_state.selected_stage = None
        st.rerun()
    
    if not stage_clients.empty:
        # Quick stats for this stage
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Clients", len(stage_clients))
        with col2:
            st.metric("Total Value", f"${stage_clients['Deal Value'].sum():,.0f}")
        with col3:
            st.metric("Avg Deal Size", f"${stage_clients['Deal Value'].mean():,.0f}")
        with col4:
            st.metric("Largest Deal", f"${stage_clients['Deal Value'].max():,.0f}")
        
        st.markdown("---")
        
        # Display clients with edit capabilities
        for idx, row in stage_clients.iterrows():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                
                with col1:
                    st.write(f"**{row['Client Name']}**")
                    st.write(f"Contact: {row['Contact Person']}")
                
                with col2:
                    st.write(f"📧 {row['Email']}")
                    st.write(f"💰 ${row['Deal Value']:,.0f}")
                
                with col3:
                    current_stage = row['Stage']
                    stage_color = STAGE_COLORS.get(current_stage, "#000000")
                    st.markdown(f"<span style='color: {stage_color}; font-weight: bold; font-size: 16px;'>●</span> {current_stage}", 
                              unsafe_allow_html=True)
                    st.write(f"Updated: {row['Last Updated']}")
                
                with col4:
                    new_stage = st.selectbox(
                        "Move to Stage", 
                        FUNNEL_STAGES, 
                        index=FUNNEL_STAGES.index(current_stage),
                        key=f"stage_move_{idx}"
                    )
                
                with col5:
                    if st.button("Update", key=f"update_stage_{idx}"):
                        st.session_state.clients_data.loc[idx, 'Stage'] = new_stage
                        st.session_state.clients_data.loc[idx, 'Last Updated'] = date.today()
                        st.success(f"Moved {row['Client Name']} to {new_stage}")
                        if new_stage != stage:
                            st.info("Client moved to different stage. Refreshing...")
                        st.rerun()
                    
                    if st.button("Delete", key=f"delete_stage_{idx}"):
                        st.session_state.clients_data = st.session_state.clients_data.drop(idx).reset_index(drop=True)
                        st.success(f"Deleted {row['Client Name']}")
                        st.rerun()
            
            st.divider()
    else:
        st.info(f"No clients in {stage} stage.")
        if st.button("Add Client to This Stage", key="add_to_stage"):
            st.session_state.current_page = "Client Management"
            st.rerun()

def main():
    st.title("🎯 Interactive Pre-Sales Funnel Dashboard")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    
    # Update page selection to include stage view
    if st.session_state.current_page == "Stage View":
        page_options = ["Dashboard", "Client Management", "Analytics", f"Stage View: {st.session_state.selected_stage}"]
        default_index = 3
    else:
        page_options = ["Dashboard", "Client Management", "Analytics"]
        default_index = page_options.index(st.session_state.current_page) if st.session_state.current_page in page_options else 0
    
    page = st.sidebar.selectbox("Choose a page", page_options, index=default_index)
    
    # Update current page
    if page.startswith("Stage View:"):
        st.session_state.current_page = "Stage View"
    else:
        st.session_state.current_page = page
        if page != "Stage View":
            st.session_state.selected_stage = None
    
    df = st.session_state.clients_data
    
    if st.session_state.current_page == "Dashboard":
        st.header("Funnel Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Clients", len(df))
        
        with col2:
            total_value = df['Deal Value'].sum()
            st.metric("Total Pipeline Value", f"${total_value:,.0f}")
        
        with col3:
            closed_won = len(df[df['Stage'] == 'Closed Won'])
            st.metric("Closed Won", closed_won)
        
        with col4:
            if len(df) > 0:
                conversion_rate = (closed_won / len(df)) * 100
                st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
        
        st.markdown("---")
        
        # Interactive stage cards
        create_stage_cards(df)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns([2, 1])
        
        with col1:
            funnel_fig = create_interactive_funnel_chart(df)
            st.plotly_chart(funnel_fig, use_container_width=True)
            
            # Note about interactivity
            st.info("💡 **Tip**: Click on funnel stages above or use the stage cards to view clients in each stage!")
        
        with col2:
            st.subheader("Stage Summary")
            stage_counts = df['Stage'].value_counts()
            for stage in FUNNEL_STAGES:
                count = stage_counts.get(stage, 0)
                if count > 0:
                    color = STAGE_COLORS[stage]
                    if st.button(f"● {stage}: {count}", key=f"summary_{stage}"):
                        st.session_state.selected_stage = stage
                        st.session_state.current_page = "Stage View"
                        st.rerun()
        
        # Deal value chart
        deal_fig = create_deal_value_chart(df)
        selected_points = st.plotly_chart(deal_fig, use_container_width=True, on_select="rerun")
        
        # Handle chart clicks
        if selected_points and hasattr(selected_points, 'selection') and selected_points.selection.points:
            clicked_stage = selected_points.selection.points[0]['x']
            st.session_state.selected_stage = clicked_stage
            st.session_state.current_page = "Stage View"
            st.rerun()
    
    elif st.session_state.current_page == "Stage View" and st.session_state.selected_stage:
        display_stage_clients(df, st.session_state.selected_stage)
    
    elif st.session_state.current_page == "Client Management":
        st.header("Client Management")
        
        # Add new client
        with st.expander("Add New Client"):
            with st.form("add_client_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_client = st.text_input("Client Name")
                    new_contact = st.text_input("Contact Person")
                    new_email = st.text_input("Email")
                
                with col2:
                    new_stage = st.selectbox("Stage", FUNNEL_STAGES)
                    new_value = st.number_input("Deal Value ($)", min_value=0, value=0)
                
                if st.form_submit_button("Add Client"):
                    if new_client and new_contact:
                        new_row = pd.DataFrame({
                            'Client Name': [new_client],
                            'Stage': [new_stage],
                            'Contact Person': [new_contact],
                            'Email': [new_email],
                            'Deal Value': [new_value],
                            'Last Updated': [date.today()]
                        })
                        st.session_state.clients_data = pd.concat([df, new_row], ignore_index=True)
                        st.success("Client added successfully!")
                        st.rerun()
        
        # Filter clients
        st.subheader("All Clients")
        
        col1, col2 = st.columns(2)
        with col1:
            stage_filter = st.multiselect("Filter by Stage", FUNNEL_STAGES, default=FUNNEL_STAGES)
        with col2:
            search_term = st.text_input("Search clients", placeholder="Enter client name...")
        
        # Apply filters
        filtered_df = df[df['Stage'].isin(stage_filter)]
        if search_term:
            filtered_df = filtered_df[filtered_df['Client Name'].str.contains(search_term, case=False, na=False)]
        
        # Display and edit clients
        if not filtered_df.empty:
            for idx, row in filtered_df.iterrows():
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                    
                    with col1:
                        st.write(f"**{row['Client Name']}**")
                        st.write(f"Contact: {row['Contact Person']}")
                    
                    with col2:
                        st.write(f"Email: {row['Email']}")
                        st.write(f"Value: ${row['Deal Value']:,.0f}")
                    
                    with col3:
                        current_stage = row['Stage']
                        stage_color = STAGE_COLORS.get(current_stage, "#000000")
                        st.markdown(f"<span style='color: {stage_color}; font-weight: bold;'>●</span> {current_stage}", 
                                  unsafe_allow_html=True)
                    
                    with col4:
                        new_stage = st.selectbox(
                            "Change Stage", 
                            FUNNEL_STAGES, 
                            index=FUNNEL_STAGES.index(current_stage),
                            key=f"stage_{idx}"
                        )
                    
                    with col5:
                        if st.button("Update", key=f"update_{idx}"):
                            st.session_state.clients_data.loc[idx, 'Stage'] = new_stage
                            st.session_state.clients_data.loc[idx, 'Last Updated'] = date.today()
                            st.success(f"Updated {row['Client Name']}")
                            st.rerun()
                        
                        if st.button("Delete", key=f"delete_{idx}"):
                            st.session_state.clients_data = st.session_state.clients_data.drop(idx).reset_index(drop=True)
                            st.success(f"Deleted {row['Client Name']}")
                            st.rerun()
                
                st.divider()
        else:
            st.info("No clients found matching the criteria.")
    
    elif st.session_state.current_page == "Analytics":
        st.header("Analytics & Insights")
        
        # Stage progression analysis
        st.subheader("Pipeline Health")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Average deal value by stage
            avg_deal_by_stage = df.groupby('Stage')['Deal Value'].mean().reset_index()
            fig = px.bar(
                avg_deal_by_stage,
                x='Stage',
                y='Deal Value',
                title="Average Deal Value by Stage",
                color='Stage',
                color_discrete_map=STAGE_COLORS
            )
            fig.update_layout(xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Client distribution pie chart
            fig = px.pie(
                df, 
                names='Stage', 
                title="Client Distribution by Stage",
                color='Stage',
                color_discrete_map=STAGE_COLORS
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed statistics
        st.subheader("Detailed Statistics")
        
        stats_df = df.groupby('Stage').agg({
            'Client Name': 'count',
            'Deal Value': ['sum', 'mean', 'max', 'min']
        }).round(2)
        
        stats_df.columns = ['Client Count', 'Total Value', 'Avg Value', 'Max Value', 'Min Value']
        stats_df = stats_df.reset_index()
        
        st.dataframe(stats_df, use_container_width=True)
        
        # Export functionality
        st.subheader("Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f"clients_data_{date.today()}.csv",
                mime="text/csv"
            )
        
        with col2:
            json_data = df.to_json(orient='records', date_format='iso')
            st.download_button(
                label="Download as JSON",
                data=json_data,
                file_name=f"clients_data_{date.today()}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()