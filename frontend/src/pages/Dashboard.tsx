import {
    Box,
    MenuItem,
    Stack,
    TextField,
} from '@mui/material';

import { Skeleton } from "@andritzot/metris-web-ui/feedback/skeleton";

import { Button} from '@andritzot/metris-web-ui/inputs/button';
import { ButtonGroup} from '@andritzot/metris-web-ui/inputs/button-group';

import { Typography } from '@andritzot/metris-web-ui/data-display/typography';
import { Panels } from '@andritzot/metris-web-ui/layout/panels';

import FiltersPanel from '../components/FiltersPanel';
import ProductionGraph from '../components/ProductionGraph';
import SegmentDetails from "../components/SegmentDetails";
import ProductionUnitDetails from "../components/ProductionUnitDetails";
import ProductivityStatistics from "../components/ProductivityStatistics";

import {
    getProductionMonth,
    getProductionStatistics,
} from "../api/productionApi";

import type {
    ProductionMonth,
    ProductionStatistics,
} from "../types/Production";

import {useEffect, useMemo, useState } from 'react';

const months = [
    { value: 1, label: "January" },
    { value: 2, label: "February" },
    { value: 3, label: "March" },
    { value: 4, label: "April" },
    { value: 5, label: "May" },
    { value: 6, label: "June" },
    { value: 7, label: "July" },
    { value: 8, label: "August" },
    { value: 9, label: "September" },
    { value: 10, label: "October" },
    { value: 11, label: "November" },
    { value: 12, label: "December" },
];

const years = [
    2025,
    2026,
];

export default function Dashboard() {

    // --------------------------------------------------
    // State
    // --------------------------------------------------

    const [displayedMonth, setDisplayedMonth] =
        useState(1);

    const [displayedYear, setDisplayedYear] =
        useState(2026);

    const [productionMonth, setProductionMonth] =
        useState<ProductionMonth | null>(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState<string | null>(null);

    const [selectedSegmentId, setSelectedSegmentId] =
        useState<string | null>(null);


    // --------------------------------------------------
    // Load production data
    // --------------------------------------------------

    useEffect(() => {

        async function loadMonth() {

            setLoading(true);
            setError(null);

            try {

                const data = await getProductionMonth(
                    displayedMonth,
                    displayedYear,
                );

                setProductionMonth(data);

            } catch (err) {

                console.error(
                    "Failed to load production data:",
                    err,
                );

                setProductionMonth(null);

                setError(
                    "Failed to load production data.",
                );

            } finally {

                setLoading(false);

            }
        }

        loadMonth();

    }, [displayedMonth, displayedYear]);


    // --------------------------------------------------
    // Derived data
    // --------------------------------------------------

    const segments =
        productionMonth?.segments ?? [];

    const orderedSegmentIds = useMemo(
        () =>
            [...segments]
                .sort(
                    (a, b) =>
                        a.startTime.getTime() -
                        b.startTime.getTime(),
                )
                .map(
                    segment =>
                        segment.segmentId,
                ),
        [segments],
    );


    // --------------------------------------------------
    // Reset selection when month/data changes
    // --------------------------------------------------

    useEffect(() => {

        if (orderedSegmentIds.length === 0) {
            setSelectedSegmentId(null);
            return;
        }

        setSelectedSegmentId(
            orderedSegmentIds[0],
        );

    }, [orderedSegmentIds]);


    // --------------------------------------------------
    // Selected segment
    // --------------------------------------------------

    const selectedSegment =
        segments.find(
            segment =>
                segment.segmentId ===
                selectedSegmentId,
        ) ?? null;


    const selectedProductionUnit =
        productionMonth?.productionUnits.find(
            productionUnit =>
                productionUnit.prodId ===
                selectedSegment?.prodId,
        ) ?? null;

    const selectedProductionId =
    segments.find(
        segment =>
            segment.segmentId === selectedSegmentId,
    )?.prodId ?? null;


    // --------------------------------------------------
    // Statistics
    // --------------------------------------------------

const [statistics, setStatistics] =
    useState<ProductionStatistics | null>(null);

useEffect(() => {
    if (!selectedSegmentId) {
        setStatistics(null);
        return;
    }

    const segmentId = selectedSegmentId;

    async function loadStatistics() {
        try {
            const data =
                await getProductionStatistics(
                    displayedMonth,
                    displayedYear,
                    segmentId,
                );

            setStatistics(data);

        } catch (error) {
            console.error(
                "Failed to load production statistics:",
                error,
            );
            setStatistics(null);
        }
    }

    loadStatistics();

}, [
    displayedMonth,
    displayedYear,
    selectedSegmentId,
]);




    // --------------------------------------------------
    // Navigation
    // --------------------------------------------------

    const selectedIndex =
        orderedSegmentIds.indexOf(
            selectedSegmentId ?? "",
        );


    function selectNextSegment() {

        if (
            selectedIndex < 0 ||
            selectedIndex >=
                orderedSegmentIds.length - 1
        ) {
            return;
        }

        setSelectedSegmentId(
            orderedSegmentIds[
                selectedIndex + 1
            ],
        );
    }


    function selectPreviousSegment() {

        if (selectedIndex <= 0) {
            return;
        }

        setSelectedSegmentId(
            orderedSegmentIds[
                selectedIndex - 1
            ],
        );
    }


    // --------------------------------------------------
    // Loading / error states
    // --------------------------------------------------


    if (error) {
        return (
            <div>
                {error}
            </div>
        );
    }


    if (!productionMonth) {
        return (
            <div>
                No production data available.
            </div>
        );
    }

if (!productionMonth && loading) {
    return (
        <Box sx={{ p: 3 }}>
            <Stack spacing={3}>
                <Skeleton
                    variant="rounded"
                    width="100%"
                    height={80}
                />

                <Skeleton
                    variant="rectangular"
                    width="100%"
                    height={400}
                />
            </Stack>
        </Box>
    );
}

    // --------------------------------------------------
    // UI
    // --------------------------------------------------

    return (
        <Box sx={{ p: 3, display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                    gap: 2,
                    flexWrap: 'wrap',
                    p: 3,
                    borderRadius: 3,
                    bgcolor: 'background.paper',
                    boxShadow: '0 1px 5px rgba(0, 0, 0, 0.05), 0 2px 5px rgba(0, 0, 0, 0.05)',
                }}
            >
                <Box>
                    <Typography variant="h5">Production Dashboard</Typography>
                </Box>

                <Box
                        sx={{
                            display: "flex",
                            gap: 1.5,
                            flexWrap: "wrap",
                            alignItems: "center",
                        }}
                    >
                        <TextField
                            select
                            size="small"
                            label="Month"
                            value={displayedMonth}
                            onChange={(event) => {
                                setDisplayedMonth(
                                    Number(event.target.value),
                                );
                            }}
                            sx={{ minWidth: 150 }}
                        >
                            {months.map((month) => (
                                <MenuItem
                                    key={month.value}
                                    value={month.value}
                                >
                                    {month.label}
                                </MenuItem>
                            ))}
                        </TextField>

                        <TextField
                            select
                            size="small"
                            label="Year"
                            value={displayedYear}
                            onChange={(event) => {
                                setDisplayedYear(
                                    Number(event.target.value),
                                );
                            }}
                            sx={{ minWidth: 120 }}
                        >
                            {years.map((year) => (
                                <MenuItem
                                    key={year}
                                    value={year}
                                >
                                    {year}
                                </MenuItem>
                            ))}
                        </TextField>
                    </Box>
            </Box>

            <Panels.Group orientation="horizontal" autoSaveId="production-dashboard-layout">
                <Panels.Item defaultSize="24%" minSize="18%" surface>
                    <FiltersPanel />
                </Panels.Item>

                <Panels.Separator />

                <Panels.Item defaultSize="46%" minSize="34%" surface>
                    <Stack spacing={3} sx={{ height: '100%' }}>
                        
                        <ProductionGraph
    data={segments}
    selectedSegmentId={selectedSegmentId}
    selectedProductionId={selectedProductionId}
    displayedMonth = {displayedMonth}
    displayedYear={displayedYear}
    loading={loading}
    
/>
                        <SegmentDetails
                            segment={selectedSegment}
                        />

                    </Stack>
                </Panels.Item>

                <Panels.Separator />

                <Panels.Item defaultSize="30%" minSize="24%" surface>
                    <Stack spacing={3} sx={{ height: '100%' }}>
                        <ButtonGroup size="small">
                        <Button onClick={selectPreviousSegment}>
                            ◀ Previous
                        </Button>
                        <Button onClick={selectNextSegment}>
                            Next ▶
                        </Button>

                        </ButtonGroup>
                        <ProductivityStatistics
                            statistics={statistics}
                        />
                    
                        <ProductionUnitDetails
                            productionUnit={selectedProductionUnit}
                        />

                    </Stack>
                </Panels.Item>
            </Panels.Group>
        </Box>
    );
}