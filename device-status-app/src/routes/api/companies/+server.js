export async function GET() {
  const companies = await fetch('http://localhost:5000/api/companies'); // Flask endpoint
  return new Response(JSON.stringify(await companies.json()), { status: 200 });
}

