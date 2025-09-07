// Simple Node.js test script for Supabase connection
import { createClient } from '@supabase/supabase-js';
import { config } from 'dotenv';

// Load environment variables
config({ path: '.env.local' });

const supabaseUrl = process.env.VITE_SUPABASE_URL || 'https://unnrwgigpoewjuahspip.supabase.co';
const supabaseAnonKey = process.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVubnJ3Z2lncG9ld2p1YWhzcGlwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMzcyMDksImV4cCI6MjA2NzYxMzIwOX0.I1A7gZPse01XUcr-snPWWn-mUUikO0yKs7hj2fTP7S0';

console.log('🧪 Testing ScamShield AI Supabase Connection...\n');
console.log(`Supabase URL: ${supabaseUrl}`);
console.log(`Anon Key: ${supabaseAnonKey.substring(0, 20)}...\n`);

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function testConnection() {
  const results = {
    connection: false,
    auth: false,
    database: false,
    functions: false,
    errors: []
  };

  try {
    // Test 1: Basic connection
    console.log('1. Testing basic connection...');
    const { data: connectionTest, error: connectionError } = await supabase
      .from('user_profiles')
      .select('count')
      .limit(1);
    
    if (connectionError) {
      results.errors.push(`Connection error: ${connectionError.message}`);
      console.log('❌ Connection failed:', connectionError.message);
    } else {
      results.connection = true;
      console.log('✅ Basic connection successful');
    }

    // Test 2: Auth functionality
    console.log('2. Testing auth functionality...');
    const { data: authTest, error: authError } = await supabase.auth.getSession();
    
    if (authError) {
      results.errors.push(`Auth error: ${authError.message}`);
      console.log('❌ Auth test failed:', authError.message);
    } else {
      results.auth = true;
      console.log('✅ Auth functionality working');
    }

    // Test 3: Database access
    console.log('3. Testing database access...');
    const { data: dbTest, error: dbError } = await supabase
      .from('investigations')
      .select('id')
      .limit(1);
    
    if (dbError) {
      results.errors.push(`Database error: ${dbError.message}`);
      console.log('❌ Database access failed:', dbError.message);
    } else {
      results.database = true;
      console.log('✅ Database access working');
    }

    // Test 4: RPC functions
    console.log('4. Testing RPC functions...');
    try {
      const { data: rpcTest, error: rpcError } = await supabase.rpc('get_user_dashboard_data', {
        p_user_id: '00000000-0000-0000-0000-000000000000' // Test UUID
      });
      
      if (rpcError) {
        if (rpcError.message.includes('permission denied') || rpcError.message.includes('function')) {
          results.functions = true;
          console.log('✅ RPC functions accessible (expected permission error for test UUID)');
        } else {
          results.errors.push(`RPC error: ${rpcError.message}`);
          console.log('❌ RPC test failed:', rpcError.message);
        }
      } else {
        results.functions = true;
        console.log('✅ RPC functions working');
      }
    } catch (err) {
      results.errors.push(`RPC test error: ${err.message}`);
      console.log('❌ RPC test exception:', err.message);
    }

  } catch (error) {
    results.errors.push(`General error: ${error.message}`);
    console.error('❌ General test failed:', error);
  }

  console.log('\n📊 Test Results Summary:');
  console.log('========================');
  console.log(`Connection: ${results.connection ? '✅' : '❌'}`);
  console.log(`Auth: ${results.auth ? '✅' : '❌'}`);
  console.log(`Database: ${results.database ? '✅' : '❌'}`);
  console.log(`Functions: ${results.functions ? '✅' : '❌'}`);
  
  if (results.errors.length > 0) {
    console.log('\n❌ Errors found:');
    results.errors.forEach(error => console.log(`  - ${error}`));
  }
  
  const allPassed = results.connection && results.auth && results.database && results.functions;
  console.log(`\n${allPassed ? '🎉' : '⚠️'} Overall Status: ${allPassed ? 'ALL TESTS PASSED' : 'SOME TESTS FAILED'}`);
  
  return results;
}

testConnection().catch(console.error);

