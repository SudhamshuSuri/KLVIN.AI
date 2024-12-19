<script>
  import { onMount } from 'svelte';
  let companies = [];
  let selectedCompany = null;
  let devices = [];
  let newDeviceName = "";

  onMount(async () => {
    const res = await fetch('http://localhost:5000/api/companies');
    companies = await res.json();
  });

  async function fetchDevices(companyId) {
    selectedCompany = companyId;
    const res = await fetch(`http://localhost:5000/api/companies/${companyId}/devices`);
    devices = await res.json();
  }

  async function addDevice() {
    if (!newDeviceName || !selectedCompany) {
      alert("Please select a company and enter a device name.");
      return;
    }

    const response = await fetch('http://localhost:5000/api/devices', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: newDeviceName,
        company_id: selectedCompany,
      })
    });

    if (response.ok) {
      newDeviceName = "";
      fetchDevices(selectedCompany); // Refresh the devices list
    } else {
      alert("Failed to add device.");
    }
  }

  // Automatically refresh devices every 10 seconds
  setInterval(() => {
    if (selectedCompany) fetchDevices(selectedCompany);
  }, 10000);

  // Determine device status dynamically
  function getDeviceStatusClass(status) {
    return status === "online" ? "online" : "offline";
  }
</script>

<!-- Dropdown to select a company -->
<select on:change="{e => fetchDevices(e.target.value)}">
  <option value="" disabled selected>Select a Company</option>
  {#each companies as company}
    <option value="{company.id}">{company.name}</option>
  {/each}
</select>

<!-- Form to add a new device -->
<div>
  <input
    type="text"
    placeholder="Enter device name"
    bind:value="{newDeviceName}"
  />
  <button on:click="{addDevice}">Add Device</button>
</div>

<!-- Display devices -->
<div class="devices">
  {#each devices as device}
    <div class="device-tile {getDeviceStatusClass(device.status)}">
      <p>{device.name}</p>
      <p>{device.last_reading}</p>
      <p>Status: {device.status}</p>
    </div>
  {/each}
</div>

<style>
  .devices {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }
  .device-tile {
    border: 1px solid #ccc;
    padding: 1rem;
    border-radius: 8px;
    width: 150px;
    text-align: center;
    transition: background-color 0.3s ease;
  }
  .online {
    background-color: #d4edda; /* Light green */
  }
  .offline {
    background-color: #f8d7da; /* Light red */
  }
</style>

