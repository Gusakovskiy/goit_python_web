
from aiomisc import entrypoint
from aiomisc.service import Profiler
import asyncio
import time


async def blocking():
    print('Blocking')
    for i in range(100):
        time.sleep(0.1)


async def hashing():
    print('Hashing')
    for _ in range(100):
        loren_ipsum = '''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tellus massa, fermentum hendrerit ornare et, molestie in sem. Aliquam magna quam, sagittis nec varius a, efficitur at urna. In at urna purus. Aliquam a faucibus odio, sit amet accumsan ex. Donec vulputate id massa porta tincidunt. Sed ipsum lorem, aliquet nec nisl sit amet, varius faucibus urna. Mauris eget efficitur tortor. Donec accumsan justo non ligula dictum, at ornare nibh venenatis. Etiam non sem a leo sagittis posuere. Vestibulum felis lectus, vestibulum ac turpis eget, porta tincidunt nisl. In quis nisl mattis, imperdiet risus venenatis, dapibus justo. Nullam interdum nec leo vel consequat. Mauris malesuada dolor ut vehicula accumsan. Vestibulum viverra aliquet odio. Mauris eget tortor nibh.

        Aenean eu molestie est. Proin pellentesque sapien ut sem consectetur, a molestie eros facilisis. Nulla ligula lectus, placerat nec hendrerit sed, viverra sed sem. Maecenas volutpat, mi imperdiet consectetur varius, erat quam laoreet metus, a lobortis felis orci vel tellus. Nulla pellentesque pulvinar sem, eget consectetur arcu interdum eget. Mauris ornare at ante eu tempus. Suspendisse elementum elit nec arcu commodo dapibus. Phasellus eget convallis nulla. Suspendisse potenti.
        
        Etiam porta est eget libero pellentesque condimentum. Aenean rhoncus, sem nec fringilla lacinia, erat lorem aliquet nulla, quis ullamcorper nunc lorem ut magna. Donec nibh neque, iaculis nec nisl vestibulum, elementum faucibus mi. Vivamus feugiat, lorem non dignissim cursus, velit ligula posuere ligula, et laoreet purus neque sed nibh. Suspendisse potenti. Maecenas pretium ultrices interdum. Aliquam finibus arcu nec lorem porttitor bibendum. Integer mollis fermentum fringilla. Vestibulum feugiat quam non pellentesque consequat. In fermentum convallis venenatis. Duis et tortor feugiat, mollis ex id, iaculis orci. Fusce aliquet mauris a enim consectetur, ut convallis nibh imperdiet. Maecenas sed bibendum elit. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Curabitur viverra mauris vulputate sem dapibus, congue scelerisque odio scelerisque. In convallis sit amet dui tincidunt vulputate.
        
        Maecenas pellentesque lectus a lobortis molestie. Fusce eleifend lacinia odio, vel porta quam interdum eu. Phasellus rhoncus laoreet dolor. Suspendisse justo justo, scelerisque ut efficitur ac, mattis ac justo. Quisque ullamcorper neque id rhoncus suscipit. Aliquam enim neque, condimentum non iaculis lacinia, suscipit rutrum odio. Etiam non sollicitudin libero, vulputate laoreet erat. Aenean vitae elementum sapien. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Ut eleifend, enim ac efficitur mattis, lectus augue egestas augue, quis condimentum arcu dolor quis nunc. Praesent ullamcorper auctor massa, ut vehicula neque lobortis nec. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut nec vestibulum dolor. Aliquam dictum, purus non dignissim hendrerit, dolor libero ultricies est, vel semper dolor massa vel ipsum. Nunc facilisis metus pellentesque volutpat bibendum.
        
        Integer arcu lorem, laoreet eu maximus sit amet, iaculis in nisl. Fusce dignissim ex ultrices sapien eleifend, quis ultrices nisl euismod. Pellentesque egestas, sem quis feugiat tincidunt, nisl risus commodo velit, tempor scelerisque lacus ligula eget orci. Cras semper ornare mauris in auctor. Suspendisse venenatis sit amet mauris in mollis. Duis semper interdum faucibus. Aenean sodales, leo eget sagittis egestas, urna dolor tempor quam, eget accumsan lorem felis nec libero. Sed interdum molestie pharetra. Integer nunc lectus, cursus sit amet tempor ut, consequat at orci. Mauris in ante in nisl vehicula faucibus. Donec ac justo risus. Maecenas accumsan nibh vel velit molestie ultrices. Morbi ut consequat felis, eu pellentesque nisi. Vivamus bibendum nibh id consequat fringilla. Nulla facilisi. Etiam in pulvinar ipsum, sed vestibulum ipsum.
        '''
        hash(loren_ipsum)


async def main():
    print('Hi')
    await asyncio.gather(
        hashing(),
        blocking()
    )
    print('End')

if __name__ == '__main__':
    with entrypoint(Profiler(interval=0.1, top_results=10), debug=True) as et:
        et.run_until_complete(main())
    # asyncio.run(main())


