import { Box, Button, Divider, MenuItem, Stack, TextField } from '@mui/material';

import { Typography } from '@andritzot/metris-web-ui/data-display/typography';

import { dashboardMonths } from '../api/production';

const lineOptions = ['All lines', 'Line 1', 'Line 2', 'Line 3', 'Line 4'];
const statusOptions = ['All statuses', 'Complete', 'Review', 'Queued'];

export default function FiltersPanel() {
    return (
        <Stack spacing={2.5} sx={{ height: '100%' }}>
            <Box>
                <Typography variant="h6">Filters</Typography>
                <Typography variant="body2" color="text.secondary">
                    Select the reporting context for the monthly overview.
                </Typography>
            </Box>

            <Stack spacing={2}>
                <TextField select label="Month" defaultValue={dashboardMonths[1].value} size="small" fullWidth>
                    {dashboardMonths.map((month) => (
                        <MenuItem key={month.value} value={month.value}>
                            {month.label}
                        </MenuItem>
                    ))}
                </TextField>

                <TextField select label="Production line" defaultValue={lineOptions[0]} size="small" fullWidth>
                    {lineOptions.map((line) => (
                        <MenuItem key={line} value={line}>
                            {line}
                        </MenuItem>
                    ))}
                </TextField>

                <TextField select label="Batch status" defaultValue={statusOptions[0]} size="small" fullWidth>
                    {statusOptions.map((status) => (
                        <MenuItem key={status} value={status}>
                            {status}
                        </MenuItem>
                    ))}
                </TextField>
            </Stack>

            <Divider />

            <Stack spacing={1.5}>
                <Typography variant="subtitle2">Quick actions</Typography>
                <Button variant="contained" fullWidth>
                    Refresh layout
                </Button>
                <Button variant="outlined" fullWidth>
                    Save dashboard view
                </Button>
            </Stack>
        </Stack>
    );
}