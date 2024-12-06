<script >
  import { onMount } from 'svelte';
  import { fetchCompanies, fetchDevices } from '$lib/api';

  let companies = [];
  let selectedCompany = null;
  let devices = [];

  async function loadCompanies() {
    try {
      companies = await fetchCompanies();
    } catch (error) {
      console.error('Error fetching companies:', error);
    }
  }

  async function loadDevices(companyId) {
    try {
      selectedCompany = companyId;
      devices = await fetchDevices(companyId);
    } catch (error) {
      console.error('Error fetching devices:', error);
    }
  }

  onMount(() => {
    loadCompanies();
  });

  setInterval(() => {
    if (selectedCompany) {
      loadDevices(selectedCompany);
    }
  }, 10000); // Refresh every 10 seconds
</script>

<main>
  <h1>Device Status Dashboard</h1>
  <label>
    Select Company:
    <select on:change={(e) => loadDevices(e.target.value)}>
      <option value="" disabled selected>Select a company</option>
      {#each companies as company}
        <option value={company.id}>{company.name}</option>
      {/each}
    </select>
  </label>

  <div class="device-grid">
    {#each devices as device}
      <div class="device-tile {device.status}" title="{device.status}">
        <h3>{device.name}</h3>
        <p>Status: {device.status}</p>
      </div>
    {/each}
  </div>
</main>

<style>
  .device-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }
  .device-tile {
    border: 2px solid;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
  }
  .device-tile.online {
    border-color: green;
  }
  .device-tile.offline {
    border-color: red;
  }
</style>

