import { Box, CardContent, Chip, Divider, Stack } from '@mui/material';

import { Typography } from '@andritzot/metris-web-ui/data-display/typography';
import { Card } from '@andritzot/metris-web-ui/surfaces/card';

import { overviewMetrics } from '../api/production';

const toneStyles = {
    positive: {
        backgroundColor: 'rgba(22, 163, 74, 0.12)',
        color: '#166534',
    },
    neutral: {
        backgroundColor: 'rgba(37, 99, 235, 0.12)',
        color: '#1d4ed8',
    },
    warning: {
        backgroundColor: 'rgba(217, 119, 6, 0.12)',
        color: '#b45309',
    },
} as const;

export default function OverviewCards() {
    return (
        <Box
            sx={{
                display: 'grid',
                gap: 2,
                gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            }}
        >
            {overviewMetrics.map((metric) => (
                <Card
                    key={metric.label}
                    variant="outlined"
                    sx={{
                        height: '100%',
                        borderRadius: 3,
                        borderColor: 'divider',
                        background:
                            'linear-gradient(180deg, rgba(63, 47, 47, 0.9) 0%, rgba(16, 22, 36, 0.92) 100%)',
                    }}
                >
                    <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
                        <Stack spacing={1.5}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 1 }}>
                                <Typography variant="subtitle2" sx={{ letterSpacing: 0.6, textTransform: 'uppercase' }}>
                                    {metric.label}
                                </Typography>
                                <Chip
                                    size="small"
                                    label={metric.tone}
                                    sx={{
                                        borderRadius: 999,
                                        ...toneStyles[metric.tone],
                                    }}
                                />
                            </Box>
                            <Typography variant="h4" sx={{ fontWeight: 700, lineHeight: 1 }}>
                                {metric.value}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                                {metric.trend}
                            </Typography>
                            <Divider />
                            <Typography variant="body3" color="text.secondary">
                                {metric.note}
                            </Typography>
                        </Stack>
                    </CardContent>
                </Card>
            ))}
        </Box>
    );
}