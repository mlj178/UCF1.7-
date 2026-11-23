using System.Collections.Generic;
using UnityEngine;

public class MapManager : Singleton<MapManager>
{
	[SerializeField]
	private SpawnPointDictionary pointDic;

	private SpawnPoint[] SP_BL;

	private SpawnPoint[] SP_GR;

	private SpawnPoint[] SP_Netural;

	private SpawnPoint[] SP_SupplyBox;

	private SpawnPoint[] SP_RedBox;

	private SpawnPoint[] SP_BlueBox;

	private static int SPID_BL;

	private static int SPID_GR;

	private static int SPID_Netural;

	private List<int> IDList_SupplyBox;

	private List<int> IDList_RedBox;

	private List<int> IDList_BlueBox;

	[SerializeField]
	public int mapGunIndex;

	public static Vector2Int mapGunAmmo;

	public bool knifeHitStun;

	public Texture2D minimap;

	public Vector3 radarOriginPos;

	public float pixelPerDistance;

	protected override void Awake()
	{
	}

	protected override void OnDestroy()
	{
	}

	private void MapGunInit()
	{
	}

	private void NewGameRoundStart()
	{
	}

	public static SpawnPoint GetSpawnPoint(Team team)
	{
		return default;
	}

	private void OnDrawGizmos()
	{
	}

	public static int GetSupplyBoxPoint(out SpawnPoint point, SupplyBox.Type type)
	{
		point = default;
		return 0;
	}

	public static void ReleaseSupplyBoxPoint(int index, SupplyBox.Type boxType)
	{
	}
}
