// Standalone test script for Supabase connection
import { runAllTests } from './src/lib/test-connection.js';

async function main() {
  try {
    await runAllTests();
  } catch (error) {
    console.error('Test script failed:', error);
    process.exit(1);
  }
}

main();

