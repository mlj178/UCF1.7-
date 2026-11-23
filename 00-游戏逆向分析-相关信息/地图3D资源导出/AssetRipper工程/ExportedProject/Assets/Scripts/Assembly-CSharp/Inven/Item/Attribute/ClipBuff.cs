using System;

namespace Inven.Item.Attribute
{
	[Serializable]
	public class ClipBuff : ItemAttributeBase
	{
		public WeaponClass wpnClass;

		public int count;

		public void Calculate(ClientData client, bool add)
		{
		}
	}
}
