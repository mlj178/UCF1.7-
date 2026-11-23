using System.Collections.Generic;
using UnityEngine;

public class HUD_GaugeSystem : Singleton<HUD_GaugeSystem>
{
	private Dictionary<string, HUD_Gauge> gaugeDic;

	public static HUD_Gauge GetGauge(GameObject prefab)
	{
		return null;
	}

	public static bool BreakGauge(string gaugeName)
	{
		return false;
	}
}
