import { Box, Button, Divider, Stack } from '@mui/material';

import { Typography } from '@andritzot/metris-web-ui/data-display/typography';
import { Card } from '@andritzot/metris-web-ui/surfaces/card';

import { reportActions } from '../api/production';

export default function ReportControls() {
    return (
        <Card variant="outlined" sx={{ borderRadius: 3, borderColor: 'divider', boxShadow: 'none' }}>
            <Stack spacing={2.5} sx={{ p: 2.5 }}>
                <Box>
                    <Typography variant="h6">Report generation</Typography>
                    <Typography variant="body2" color="text.secondary">
                        Phase 1 controls for the future export workflow.
                    </Typography>
                </Box>

                <Stack spacing={1.25}>
                    <Button variant="contained" fullWidth>
                        Generate report
                    </Button>
                    <Button variant="outlined" fullWidth>
                        Export batch data
                    </Button>
                </Stack>

                <Divider />

                <Stack spacing={1.5}>
                    {reportActions.map((action) => (
                        <Box key={action.label}>
                            <Typography variant="subtitle2">{action.label}</Typography>
                            <Typography variant="body3" color="text.secondary">
                                {action.description}
                            </Typography>
                        </Box>
                    ))}
                </Stack>
            </Stack>
        </Card>
    );
}