"""Curated, representative NSE ticker universes by market-cap band.

DATA PROVENANCE: the official NSE index factsheets and constituent files
(nseindia.com, nsearchives.nseindia.com) and every third-party mirror tried
(Screener, smart-investing.in) were unreachable from this environment. These
lists are NOT a live scrape of the official Nifty 50 / Midcap 100 / Smallcap
250 / Microcap 250 index membership -- they are a hand-curated, general-
knowledge approximation of each band, used only to give the daily picker a
representative sample to draw from. NIFTY_50 is reasonably reliable (large,
stable, well-known constituents change rarely). The other three bands are a
representative subset, not a complete or currently-exact index membership,
and should be refreshed periodically. State this caveat in every report
generated from a pick made against these lists.
"""

NIFTY_50 = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS",
    "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "BAJFINANCE.NS",
    "KOTAKBANK.NS", "LT.NS", "HCLTECH.NS", "AXISBANK.NS", "ASIANPAINT.NS",
    "MARUTI.NS", "TITAN.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "WIPRO.NS",
    "NESTLEIND.NS", "BAJAJFINSV.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS",
    "M&M.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "ADANIENT.NS", "ADANIPORTS.NS",
    "COALINDIA.NS", "JSWSTEEL.NS", "GRASIM.NS", "HINDALCO.NS", "TECHM.NS",
    "DRREDDY.NS", "CIPLA.NS", "DIVISLAB.NS", "APOLLOHOSP.NS", "BRITANNIA.NS",
    "EICHERMOT.NS", "HEROMOTOCO.NS", "BAJAJ-AUTO.NS", "SBILIFE.NS", "HDFCLIFE.NS",
    "INDUSINDBK.NS", "BPCL.NS", "SHREECEM.NS", "UPL.NS", "TATACONSUM.NS",
]

# Representative sample, not the exact current official Nifty Midcap 100 list.
NIFTY_MIDCAP_100_SAMPLE = [
    "PERSISTENT.NS", "ASTRAL.NS", "DIXON.NS", "PAGEIND.NS", "COFORGE.NS",
    "AUROPHARMA.NS", "BALKRISIND.NS", "CUMMINSIND.NS", "MPHASIS.NS", "TATAELXSI.NS",
    "VOLTAS.NS", "GODREJPROP.NS", "OBEROIRLTY.NS", "PIIND.NS", "SRF.NS",
    "ALKEM.NS", "LUPIN.NS", "TORNTPOWER.NS", "IDFCFIRSTB.NS", "FEDERALBNK.NS",
    "BANDHANBNK.NS", "AUBANK.NS", "PFC.NS", "RECLTD.NS", "INDHOTEL.NS",
    "JUBLFOOD.NS", "MRF.NS", "APOLLOTYRE.NS", "ESCORTS.NS", "BHARATFORG.NS",
    "SUPREMEIND.NS", "CROMPTON.NS", "HAVELLS.NS", "DEEPAKNTR.NS", "NAVINFLUOR.NS",
    "GLENMARK.NS", "TORNTPHARM.NS", "IPCALAB.NS", "LTF.NS", "CHOLAFIN.NS",
    "MUTHOOTFIN.NS", "SUNDARMFIN.NS", "GODFRYPHLP.NS", "EMAMILTD.NS", "COLPAL.NS",
    "ABCAPITAL.NS", "MFSL.NS", "OFSS.NS", "GMRINFRA.NS", "IRCTC.NS",
]

# Representative sample, not the exact current official Nifty Smallcap 250 list.
NIFTY_SMALLCAP_250_SAMPLE = [
    "KPRMILL.NS", "RATNAMANI.NS", "FINEORG.NS", "GRINDWELL.NS", "CARBORUNIV.NS",
    "TTKPRESTIG.NS", "VGUARD.NS", "RAJESHEXPO.NS", "ZYDUSWELL.NS", "GRANULES.NS",
    "LAURUSLABS.NS", "CAPLIPOINT.NS", "SUVENPHAR.NS", "JBCHEPHARM.NS", "AJANTPHARM.NS",
    "NEWGEN.NS", "INTELLECT.NS", "ZENSARTECH.NS", "MASTEK.NS", "KPITTECH.NS",
    "SONATSOFTW.NS", "RATEGAIN.NS", "HAPPSTMNDS.NS", "ROUTE.NS", "CYIENT.NS",
    "TIINDIA.NS", "SCHAEFFLER.NS", "TIMKEN.NS", "SKFINDIA.NS", "FIEMIND.NS",
    "SANDHAR.NS", "SUNDRMFAST.NS", "GABRIEL.NS", "ENDURANCE.NS", "MINDACORP.NS",
    "JKCEMENT.NS", "HEIDELBERG.NS", "STARCEMENT.NS", "PRINCEPIPE.NS", "APLAPOLLO.NS",
    "RAINBOW.NS", "KIMS.NS", "SHALBY.NS", "METROPOLIS.NS", "VIJAYA.NS",
    "CENTRALBK.NS", "UCOBANK.NS", "IOB.NS", "BANKINDIA.NS", "MAHABANK.NS",
]

# Representative sample, not the exact current official Nifty Microcap 250 list.
# Skewed toward names with adequate liquidity per the framework's own G0/X3
# floors (ADTV >= Rs1 Cr, mcap >= Rs250 Cr) since illiquid microcaps fail the
# very first gate and waste an analysis cycle.
NIFTY_MICROCAP_250_SAMPLE = [
    "SHARDACROP.NS", "VINATIORGA.NS", "ROSSARI.NS", "NEOGEN.NS", "GALAXYSURF.NS",
    "CHEMPLASTS.NS", "CLEAN.NS", "AETHER.NS", "JUBLPHARMA.NS", "SEQUENT.NS",
    "SOLARA.NS", "SPANDANA.NS", "UJJIVANSFB.NS", "EQUITASBNK.NS", "CSBBANK.NS",
    "DCBBANK.NS", "SOUTHBANK.NS", "KARURVYSYA.NS", "CUB.NS", "RBLBANK.NS",
    "REPCOHOME.NS", "APTUS.NS", "HOMEFIRST.NS", "AAVAS.NS", "CANFINHOME.NS",
    "GRAVITA.NS", "RHIM.NS", "ORIENTREF.NS", "VESUVIUS.NS", "HEG.NS",
    "GPIL.NS", "SHYAMMETL.NS", "JINDALSAW.NS", "RAMASTEEL.NS", "MAHASTEEL.NS",
    "ROUTE.NS", "LATENTVIEW.NS", "DATAPATTNS.NS", "TARIL.NS", "SALASAR.NS",
    "GRSE.NS", "COCHINSHIP.NS", "MAZDOCK.NS", "BEML.NS", "TITAGARH.NS",
    "RAILTEL.NS", "IRCON.NS", "RVNL.NS", "IRFC.NS", "CONCOR.NS",
]

UNIVERSES = {
    "Nifty 50": NIFTY_50,
    "Nifty Midcap 100 (representative sample)": NIFTY_MIDCAP_100_SAMPLE,
    "Nifty Smallcap 250 (representative sample)": NIFTY_SMALLCAP_250_SAMPLE,
    "Nifty Microcap 250 (representative sample)": NIFTY_MICROCAP_250_SAMPLE,
}
