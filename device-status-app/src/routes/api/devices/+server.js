export const GET = async ({ url }) => {
  const companyId = url.searchParams.get('companyId');
  if (!companyId) {
    return new Response('Company ID is required', { status: 400 });
  }

  const response = await fetch(`http://localhost:5000/api/companies/${companyId}/devices`); // Replace with Flask endpoint
  const devices = await response.json();
  return new Response(JSON.stringify(devices), { status: 200 });
};

