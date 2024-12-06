<script>
  import { onMount } from 'svelte';
  import { fetchCompanies, fetchDevices } from '$lib/api.js';

  let companies = [];
  let selectedCompany = null;
  let devices = [];

  async function loadCompanies() {
    companies = await fetchCompanies();
  }

  async function loadDevices(companyId) {
    selectedCompany = companyId;
    devices = await fetchDevices(companyId);
  }

  onMount(() => {
    loadCompanies();
  });

  // Auto-refresh every 10 seconds
  setInterval(() => {
    if (selectedCompany) {
      loadDevices(selectedCompany);
    }
  }, 10000);
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
      <div class="device-tile" style="border-color: {device.status === 'online' ? 'green' : 'red'}">
        <h3>{device.name}</h3>
        <p>Status: <span style="color: {device.status === 'online' ? 'green' : 'red'}">{device.status}</span></p>
      </div>
    {/each}
  </div>
</main>

<style>
  .device-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }
  .device-tile {
    border: 2px solid;
    padding: 1rem;
    border-radius: 0.5rem;
    text-align: center;
  }
</style>

