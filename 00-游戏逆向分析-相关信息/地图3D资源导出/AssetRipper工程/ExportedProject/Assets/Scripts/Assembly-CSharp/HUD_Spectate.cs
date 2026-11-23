using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HUD_Spectate : Singleton<HUD_Spectate>
{
	public class Data
	{
		public int spawnCount;

		public string nickName;

		public int damage;

		public HUD_SpectateMsg bindMsg;
	}

	private static readonly string hideString;

	private static readonly string showString;

	private static readonly Vector2 originPos;

	private static readonly Vector2 offsetPos;

	private static readonly Vector3 hideScale;

	[SerializeField]
	private RectTransform mainRect;

	[SerializeField]
	private Text underText;

	[SerializeField]
	private RawImage killerLevel;

	[SerializeField]
	private Text killerNameText;

	[SerializeField]
	private Text weaponNameText;

	[SerializeField]
	private RectTransform weaponRect;

	[SerializeField]
	private RawImage weaponImage;

	[SerializeField]
	private RawImage weaponExtraImage;

	[SerializeField]
	private GameObject skull;

	[SerializeField]
	private GameObject headShot;

	private bool switchCooling;

	private bool isOpen;

	public Sprite[] hitNodeSprites;

	public List<HUD_SpectateMsg> spareMsg;

	private List<HUD_SpectateMsg> busyMsg;

	private List<Data> dataList;

	protected override void Awake()
	{
	}

	private void SpawnEvent(Player player)
	{
	}

	private void DamageEvent(ref DamageEventData eventData)
	{
	}

	private void DeathEvent(DeathEventData eventData)
	{
	}

	private void KillEvent(DeathEventData eventData)
	{
	}

	private void Update()
	{
	}

	private void Clear()
	{
	}

	private void Open()
	{
	}

	private void Close()
	{
	}

	private void TryCloseAandObserveTeammate()
	{
	}
}
