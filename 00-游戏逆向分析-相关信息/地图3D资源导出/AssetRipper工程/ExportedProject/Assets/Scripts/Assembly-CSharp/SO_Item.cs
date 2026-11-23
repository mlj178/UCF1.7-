using System;
using Inven.Item.Attribute;
using UnityEngine;

[CreateAssetMenu]
public class SO_Item : ScriptableObject
{
	[Serializable]
	public enum Level
	{
		Normal = 0,
		VVIP = 1
	}

	public int index;

	public Texture itemIcon;

	public string itemName;

	public Level itemLevel;

	public bool unique;

	public ItemAttribute attributes;

	public virtual bool GetSelected()
	{
		return false;
	}

	public bool TryCalClipBuff(ClientData client, bool add)
	{
		return false;
	}
}
