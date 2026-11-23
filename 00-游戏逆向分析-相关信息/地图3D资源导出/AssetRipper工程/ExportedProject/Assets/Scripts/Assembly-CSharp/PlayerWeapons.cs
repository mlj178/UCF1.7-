using System.Collections.Generic;

public class PlayerWeapons
{
	private Player owner;

	private List<Weapon> all;

	public Weapon inUse;

	public Weapon[] current;

	public Weapon[] normal;

	public Weapon[] special;

	public Weapon temporaryWpn;

	public Weapon F_KeyWpn;

	private Weapon mapWpn;

	public bool rapidChange;

	public bool runState;

	public bool interactDisabled;

	public float movePenalty;

	public PropertyModifier Modifier_ReloadSpeed;

	public PropertyModifier Modifier_KnifeRange;

	public PropertyModifier Modifier_KnifeSpeed;

	public int curSlot { get; private set; }

	public int lastSlot { get; private set; }

	public float ReloadSpeed => 0f;

	public float KnifeRange => 0f;

	public float KnifeSpeed => 0f;

	public bool isInfinityAmmo => false;

	public PlayerWeapons(Player owner)
	{
	}

	public void AutoSelect()
	{
	}

	public int GetValidSlot()
	{
		return 0;
	}

	public bool SelectLast()
	{
		return false;
	}

	public void SelectLastOrAutoSelect()
	{
	}

	public bool Select(int slot)
	{
		return false;
	}

	public bool SelectByMouseRoll(bool forward)
	{
		return false;
	}

	public void SetWeapon(Weapon weapon)
	{
	}

	public void SelectFKeyWeapon()
	{
	}

	public void RemoveAll()
	{
	}

	public void Remove(Weapon weapon, bool recycle = true)
	{
	}

	private void SetCurrentWeapon(int slot, Weapon wpn)
	{
	}

	public void FillMainWeaponAmmo()
	{
	}

	public void FillAllGunAmmo()
	{
	}

	public void GiveUpWeapon()
	{
	}

	public void GiveUpWeapon(int slot, bool death)
	{
	}
}
