# DRAFT: Functions auto-extracted from notebooks.
# Review, de-duplicate, and move into a proper utils/ package.

# From Explatory_Data_Analysis.ipynb (cell 11): count_QSO_logs
def count_QSO_logs(callsign):
    """
    Count the number of QSO logs for a given callsign.
    """
    return logs[logs['sent_call'] == callsign].shape[0]

# From Modelling.ipynb (cell 43): cdf_fitted
def cdf_fitted(x, shape = shape, loc = loc, scale = scale):
    '''
    cdf of lognormal distribution with pre set shape, loc, and scale
    '''
    return stats.lognorm.cdf(x, shape, loc=loc, scale=scale)

# From Modelling.ipynb (cell 56): freq_to_band
def freq_to_band(freq_khz):
    """
    Convert frequency in kHz to amateur radio band name.
    
    Parameters:
        freq_khz (float): Frequency in kilohertz.
        
    Returns:
        str: Band name (e.g., '20M', '40M') or 'UNKNOWN' if not matched.
    """
    if 1800 <= freq_khz <= 2000:
        return "160M"
    
    elif 3500 <= freq_khz <= 4000:
        return "80M"
    
    elif 7000 <= freq_khz <= 7300:
        return "40M"
    
    elif 14000 <= freq_khz <= 14350:
        return "20M"
    
    elif 21000 <= freq_khz <= 21450:
        return "15M"
    
    elif 28000 <= freq_khz <= 29700:
        return "10M"
    
    else:
        return "UNKNOWN"

# From Modelling.ipynb (cell 56): form_pairs
def form_pairs(a, b):
    return tuple(sorted([a, b]))

# From Modelling.ipynb (cell 73): safe_maidenhead_distance
def safe_maidenhead_distance(locator1, locator2):
    """
    Calculate the distance between two Maidenhead locators.
    
    Parameters:
        locator1 (str): First Maidenhead locator.
        locator2 (str): Second Maidenhead locator.
        
    Returns:
        float: Distance in kilometers, or None if either locator is invalid.
    """
    try:
        if pd.isna(locator1) or pd.isna(locator2):
            return np.nan
        coord1 = mh.to_location(locator1, center=True)
        coord2 = mh.to_location(locator2, center=True)
        return haversine(coord1, coord2)
    except Exception:
        return np.nan

# From Modelling.ipynb (cell 75): midpoint_solar_time
def midpoint_solar_time(utc_timestamp, loc1, loc2):
    """
    Calculate the midpoint solar time between two locations based on their Maidenhead locators.
    
    Parameters:
        utc_timestamp (pd.Timestamp): UTC timestamp of the QSO.
        loc1 (str): Maidenhead locator of the first station.
        loc2 (str): Maidenhead locator of the second station.
        
    Returns:
        pd.Timestamp: local solar time at the midpoint.
        Returns pd.NaT if locators are invalid.
    """
    try:
        coord1 = mh.to_location(loc1, center=True)
        coord2 = mh.to_location(loc2, center=True)
        
        # Calculate midpoint coordinates
        mid_lat = (coord1[0] + coord2[0]) / 2
        mid_lon = (coord1[1] + coord2[1]) / 2
        
        # Convert to datetime
        return utc_timestamp + pd.Timedelta(hours=(mid_lon / 15))
    except Exception as e:
        return pd.NaT

# From Modelling.ipynb (cell 79): sample_by_band
def sample_by_band(df, n_samples = 20000, seed = 42):
    """
    Return a dataframe with up to `n_per_band` rows for every distinct `band`.
    Keeps the sample balanced so each band is equally represented.

    Args:
        df (_type_): _description_
        n_samples (int, optional): _description_. Defaults to 20000.
        seed (int, optional): _description_. Defaults to 42.
    """
    
    rng = np.random.default_rng(seed)
    grouped = df.groupby('band', group_keys=False)
    
    def _sample(group):
        if len(group) > n_samples:
            return group.sample(n=n_samples, random_state=rng)
        else:
            return group
        
    sampled = grouped.apply(_sample)
    return sampled.reset_index(drop=True)

# From Modelling.ipynb (cell 79): _sample
def _sample(group):
        if len(group) > n_samples:
            return group.sample(n=n_samples, random_state=rng)
        else:
            return group

# From Modelling.ipynb (cell 80): circular_distance
def circular_distance(t, t_i, period = 24.0):
    dt = np.abs(t - t_i)
    dt = np.minimum(dt, period - dt)  # Ensure circular distance
    return dt

# From Modelling.ipynb (cell 80): epan
def epan(u):
    mask = np.abs(u) <= 1
    out = np.zeros_like(u, dtype=float)
    out[mask] = 0.75 * (1 - u[mask] ** 2)
    return out

# From Modelling.ipynb (cell 80): kde2d_warped_epan
def kde2d_warped_epan(time, dist, grid_t, grid_d, h_t, h_d):
    """
    Perform 2D kernel density estimation with warped Epanechnikov kernel.
    
    Parameters:
        time (np.ndarray): Time data.
        dist (np.ndarray): Distance data.
        grid_t (np.ndarray): Grid for time.
        grid_d (np.ndarray): Grid for distance.
        h_t (float): Bandwidth for time.
        h_d (float): Bandwidth for distance.
        
    Returns:
        density: 2D array of estimated densities.
    """
    n = len(time)
    T,D = np.meshgrid(grid_t, grid_d)
    G = np.zeros_like(T, dtype=float)
    
    for t, d in zip(time, dist):
        Kt = epan(circular_distance(T, t)/ h_t) / h_t
        Kd = epan((D - d) / h_d) / h_d
        G += Kt * Kd # product of the kernels
    G /= n  # Normalize by number of points
    density = G
    
    return density

# From Modelling.ipynb (cell 100): epan
def epan(u):
    y = np.zeros_like(u); m = np.abs(u) <= 1
    y[m] = 0.75*(1-u[m]**2); return y

# From Modelling.ipynb (cell 100): kde1d_epan_reflect
def kde1d_epan_reflect(x, grid, h, a=0.0, b=None):
    x = np.asarray(x, float)
    if b is None: b = grid.max()
    xr = np.concatenate([x, -x + 2*a, -x + 2*b])  # reflect at both ends
    dens = np.zeros_like(grid, float)
    for xi in xr:
        dens += epan((grid - xi)/h) / h
    dens /= len(x)                          # divide by original sample size
    dens /= np.trapezoid(dens, grid)            # renormalise
    return dens

# From Modelling.ipynb (cell 104): epan
def epan(u):
    y = np.zeros_like(u, float)
    m = np.abs(u) <= 1
    y[m] = 0.75 * (1 - u[m]**2)
    return y

# From Modelling.ipynb (cell 104): kde1d_epan_reflect
def kde1d_epan_reflect(x, grid, h, a=0.0, b=None):
    x = np.asarray(x, float)
    if b is None: b = grid.max()
    xr = np.concatenate([x, -x + 2*a, -x + 2*b])  # reflect ends
    dens = np.zeros_like(grid, float)
    for xi in xr:
        dens += epan((grid - xi)/h) / h
    dens /= len(x)                      # divide by original sample size
    dens /= trapezoid(dens, grid)       # normalise to integrate to 1
    return dens

# From Modelling.ipynb (cell 104): make_canonical_grid_map
def make_canonical_grid_map(pos_band):
    a = pos_band[['sent_call','GRID-LOCATOR']].rename(columns={'sent_call':'call','GRID-LOCATOR':'grid'})
    b = pos_band[['rcvd_call','GRID-LOCATOR_RX']].rename(columns={'rcvd_call':'call','GRID-LOCATOR_RX':'grid'})
    locs = pd.concat([a,b], ignore_index=True).dropna()
    locs['grid'] = locs['grid'].str.strip().str.upper()
    return locs.groupby('call')['grid'].agg(lambda s: s.value_counts().idxmax())

# From Modelling.ipynb (cell 104): sample_pair_distances
def sample_pair_distances(grid_map, max_pairs=100_000, seed=42):
    calls = grid_map.index.to_numpy()
    if len(calls) < 2:
        return np.array([])
    rng = np.random.default_rng(seed)
    i = rng.choice(len(calls), size=max_pairs, replace=True)
    j = rng.choice(len(calls), size=max_pairs, replace=True)
    g1 = grid_map.iloc[i].to_numpy()
    g2 = grid_map.iloc[j].to_numpy()
    # function to compute distance between two Maidenhead locators:
    return np.array([safe_maidenhead_distance(a,b) for a,b in zip(g1,g2)], dtype=float)

# From Modelling.ipynb (cell 104): availability_baseline
def availability_baseline(pos_band, grid_t):
    hours = (pos_band['midpoint_solar_time'].dt.hour
             + pos_band['midpoint_solar_time'].dt.minute/60
             + pos_band['midpoint_solar_time'].dt.second/3600).to_numpy()
    # count unique stations per bin
    bins = np.append(grid_t, 24.0)
    
    hist, _ = np.histogram(hours, bins=bins)
    pi = hist.astype(float) + 1e-9
    pi /= trapezoid(pi, grid_t)
    return pi

