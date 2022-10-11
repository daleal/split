import { client } from '@/api/client';

export const healthCheck = () => client.get('/health-check');
