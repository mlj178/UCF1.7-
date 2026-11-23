using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HUD_HeartBeatRadar : Singleton<HUD_HeartBeatRadar>
{
	private bool open;

	[SerializeField]
	private RectTransform heartBeatWave;

	private List<Player> checkedEnemy;

	private bool scaleAnim;

	private float startScanTime;

	[SerializeField]
	private AudioClip heartBeatSnd;

	private float nextSndTime;

	[SerializeField]
	private GameObject hearBeatPrefab;

	private SimpleObjectPool pool;

	[SerializeField]
	private CommonHud_1 radarEffect;

	private void Start()
	{
	}

	private void Update()
	{
	}

	private void AddHeartBeatIcon(Player player)
	{
	}

	private float GetScanDuration()
	{
		return 0f;
	}

	private IEnumerator ScaleAnimation()
	{
		return null;
	}

	public static void PlayRadarEffect()
	{
	}
}
