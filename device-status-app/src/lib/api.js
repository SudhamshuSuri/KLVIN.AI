export async function fetchCompanies() {
  const res = await fetch('/api/companies');
  if (!res.ok) {
    throw new Error('Failed to fetch companies');
  }
  return await res.json();
}

export async function fetchDevices(companyId) {
  const res = await fetch(`/api/devices?companyId=${companyId}`);
  if (!res.ok) {
    throw new Error('Failed to fetch devices');
  }
  return await res.json();
}

