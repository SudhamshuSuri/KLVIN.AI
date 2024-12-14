<script>
  import { onMount } from 'svelte';

  let companies = [];
  let deviceName = ''; // Ensure deviceName is declared as a variable
  let selectedCompany = ''; // Variable to hold the selected company ID

  // Fetch companies when the component is mounted
  onMount(async () => {
    const response = await fetch('/api/companies');
    if (response.ok) {
      companies = await response.json();
    } else {
      console.error('Failed to fetch companies');
    }
  });

  // Submit the form
  async function addDevice(event) {
    event.preventDefault();

    if (!deviceName || !selectedCompany) {
      alert('Device name and company must be selected.');
      return;
    }

    try {
      const response = await fetch('/api/devices', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: deviceName,
          company_id: selectedCompany,
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to add device: ${response.statusText}`);
      }

      alert('Device added successfully!');
      deviceName = ''; // Reset the input field
      selectedCompany = ''; // Reset the dropdown
    } catch (error) {
      console.error('Error adding device:', error);
      alert('Error adding device.');
    }
  }
</script>

<main>
  <h1>Device Management</h1>

  <!-- Add Device Form -->
  <form on:submit={addDevice}>
    <label>
      Device Name:
      <!-- Ensure the variable is declared in the <script> -->
      <input
        type="text"
        bind:value={deviceName}
        placeholder="Enter device name"
        required
      />
    </label>

    <label>
      Select Company:
      <select bind:value={selectedCompany} required>
        <option value="" disabled selected>Select a company</option>
        {#each companies as company}
          <option value={company.id}>{company.name}</option>
        {/each}
      </select>
    </label>

    <button type="submit">Add Device</button>
  </form>
</main>

<style>
  form {
    margin: 1rem 0;
    padding: 1rem;
    border: 1px solid #ccc;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 400px;
  }

  label {
    display: flex;
    flex-direction: column;
  }

  input,
  select,
  button {
    font-size: 1rem;
    padding: 0.5rem;
  }

  button {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  button:hover {
    background-color: #0056b3;
  }
</style>

