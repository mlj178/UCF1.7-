using System.Collections.Generic;

public class ClientData
{
	public struct ClipBuffInfo
	{
		public int rifle;

		public int sniper;

		public int smg;

		public int machineGun;

		public int pistol;

		public void Clear()
		{
		}

		public void Print()
		{
		}

		public int GetCount(WeaponClass wpnClass)
		{
			return 0;
		}

		public void AddMaxClip(WPN_Gun.AmmoData ammoData, WeaponClass wpnClass)
		{
		}
	}

	public static ClientData mine;

	public int defaultWpnBagID;

	public int[][] wpnBags;

	public string nickName;

	public int level;

	public Team joinTeam;

	public bool isBot;

	public int vipLevel;

	public int character;

	public List<int> itemList;

	public ClipBuffInfo clipBuffInfo;

	public bool haveNanoCloth { get; private set; }

	public bool haveNanoAmmo { get; private set; }

	public bool haveRifleAmmo { get; private set; }

	public bool haveShotGunAmmo { get; private set; }

	public bool haveMgAmmo { get; private set; }

	public bool haveSmgAmmo { get; private set; }

	public bool haveSniperAmmo { get; private set; }

	public bool havePistolAmmo { get; private set; }

	public bool haveHulk { get; private set; }

	public bool haveNurse { get; private set; }

	public bool havePsycho { get; private set; }

	public bool haveNanoRole { get; private set; }

	public bool haveNanoHook { get; private set; }

	public void AddOrRemoveItem(int itemID)
	{
	}

	public void Update()
	{
	}

	public void BotRandom()
	{
	}

	public void CalculateClipBuff()
	{
	}
}
